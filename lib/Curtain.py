"""Send recorded WellSun curtain commands through a CC1101 on SPI1."""

import argparse
import asyncio
import ctypes
import fcntl
import json
import logging
import os
from pathlib import Path
import struct
import time


_SYNC = b"\x16\xea"
_SIGNALS = Path(__file__).with_name("curtain")


class _SpiTransfer(ctypes.Structure):
    _fields_ = [
        ("tx_buf", ctypes.c_uint64),
        ("rx_buf", ctypes.c_uint64),
        ("len", ctypes.c_uint32),
        ("speed_hz", ctypes.c_uint32),
        ("delay_usecs", ctypes.c_uint16),
        ("bits_per_word", ctypes.c_uint8),
        ("cs_change", ctypes.c_uint8),
        ("tx_nbits", ctypes.c_uint8),
        ("rx_nbits", ctypes.c_uint8),
        ("word_delay_usecs", ctypes.c_uint8),
        ("pad", ctypes.c_uint8),
    ]


class _CC1101:
    def __init__(self, device):
        if ctypes.sizeof(_SpiTransfer) != 32:
            raise RuntimeError("Unsupported SPI transfer structure")
        self.fd = os.open(device, os.O_RDWR)
        try:
            fcntl.ioctl(self.fd, 0x40016B01, struct.pack("B", 0))  # SPI mode 0
        except Exception:
            os.close(self.fd)
            raise

    def close(self):
        os.close(self.fd)

    def _transfer(self, data):
        data = bytes(data)
        tx = ctypes.create_string_buffer(data, len(data))
        rx = ctypes.create_string_buffer(len(data))
        item = _SpiTransfer(
            ctypes.addressof(tx), ctypes.addressof(rx), len(data),
            500_000, 0, 8, 0, 0, 0, 0, 0,
        )
        fcntl.ioctl(self.fd, 0x40206B00, ctypes.string_at(ctypes.addressof(item), 32))
        return rx.raw

    def strobe(self, command):
        self._transfer([command])

    def write(self, address, value):
        self._transfer([address, value])

    def read(self, address, status=False):
        return self._transfer([(0xC0 if status else 0x80) | address, 0])[1]

    def burst(self, address, payload):
        self._transfer(bytes([0x40 | address]) + bytes(payload))

    def configure(self, frequency_hz):
        self.strobe(0x30)  # SRES
        time.sleep(0.01)
        version = self.read(0x31, status=True)
        if version not in (0x14, 0x04):
            raise RuntimeError("CC1101 version read failed: 0x%02X" % version)

        word = round(frequency_hz * 65536 / 26_000_000)
        registers = {
            0x04: _SYNC[0], 0x05: _SYNC[1],
            0x06: 24, 0x07: 0x00, 0x08: 0x00,
            0x0B: 0x06, 0x0C: 0x00,
            0x0D: (word >> 16) & 0xFF,
            0x0E: (word >> 8) & 0xFF,
            0x0F: word & 0xFF,
            0x10: 0x8A, 0x11: 0x93,
            0x12: 0x12,  # GFSK, 16-bit sync
            0x13: 0x02, 0x14: 0xF8,
            0x15: 0x36,  # frequency deviation
            0x17: 0x00, 0x18: 0x18,
            0x21: 0x56, 0x22: 0x10,
        }
        self.strobe(0x36)  # SIDLE
        self.strobe(0x3B)  # SFTX
        for address, value in registers.items():
            self.write(address, value)
        self.burst(0x3E, [0x60])  # tested PA table value
        for address in (0x04, 0x05, 0x06, 0x0D, 0x0E, 0x0F, 0x10, 0x11, 0x12, 0x15):
            if self.read(address) != registers[address]:
                raise RuntimeError("CC1101 register 0x%02X readback failed" % address)

    def transmit_frame(self, payload, preamble_ms):
        self.write(0x06, len(payload))  # PKTLEN
        self.strobe(0x35)  # STX with an empty FIFO emits alternating preamble
        deadline = time.monotonic() + 0.3
        while time.monotonic() < deadline:
            state = self.read(0x35, status=True) & 0x1F
            if state == 0x13:
                break
            time.sleep(0.001)
        else:
            raise RuntimeError("CC1101 did not enter TX (state 0x%02X)" % state)

        time.sleep(preamble_ms / 1000)
        self.burst(0x3F, payload)  # sync and payload follow the preamble
        deadline = time.monotonic() + 0.5
        while time.monotonic() < deadline:
            state = self.read(0x35, status=True) & 0x1F
            if state == 0x01:
                break
            if state == 0x16:
                raise RuntimeError("CC1101 TX FIFO underflow")
            time.sleep(0.001)
        else:
            raise RuntimeError("CC1101 TX timed out (state 0x%02X)" % state)
        if self.read(0x3A, status=True) != 0:
            raise RuntimeError("CC1101 TX FIFO is not empty")


class Curtain:
    """Send up, down and stop commands; movement scheduling belongs to the caller.

    The default frequency compensates for the measured offset of the tested
    CC1101 board. It may need recalibration for another board.
    """

    def __init__(self, device="/dev/spidev1.0", frequency_hz=433_942_444):
        self.device = device
        self.frequency_hz = frequency_hz
        self._frames = {
            command: self._load_signal(_SIGNALS / (command + ".json"))
            for command in ("up", "down", "stop")
        }

    @staticmethod
    def _load_signal(path):
        with path.open() as file:
            sequence = json.load(file)
        if not isinstance(sequence, list) or not sequence:
            raise ValueError("Empty curtain signal: %s" % path)

        frames = []
        for frame in sequence:
            raw = bytes.fromhex(frame["hex"])
            sync_ms = float(frame["sync_ms"])
            preamble_ms = float(frame["preamble_ms"])
            if len(raw) != 26 or raw[:2] != _SYNC:
                raise ValueError("Invalid curtain frame in %s" % path)
            if sync_ms < 0 or preamble_ms < 0 or (frames and sync_ms <= frames[-1][0]):
                raise ValueError("Invalid curtain frame timing in %s" % path)
            frames.append((sync_ms, preamble_ms, raw[2:]))
        return tuple(frames)

    def _send(self, command):
        frames = self._frames[command]
        radio = _CC1101(self.device)
        try:
            radio.configure(self.frequency_hz)
            reference = time.monotonic()
            first_sync_ms, first_preamble_ms, _ = frames[0]
            for sync_ms, preamble_ms, payload in frames:
                start = reference + (
                    sync_ms - first_sync_ms - preamble_ms + first_preamble_ms
                ) / 1000
                delay = start - time.monotonic()
                if delay > 0:
                    time.sleep(delay)
                radio.transmit_frame(payload, preamble_ms)
        finally:
            try:
                radio.strobe(0x36)  # SIDLE
                radio.strobe(0x3B)  # SFTX
            finally:
                radio.close()
        logging.info("Curtain RF command transmitted: %s", command)

    async def up(self):
        self._send("up")

    async def down(self):
        self._send("down")

    async def stop(self):
        self._send("stop")


def main():
    parser = argparse.ArgumentParser(description="Send one curtain command over CC1101")
    parser.add_argument("command", choices=("up", "down", "stop"))
    parser.add_argument("--device", default="/dev/spidev1.0")
    parser.add_argument("--frequency-hz", type=int, default=433_942_444)
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO)
    curtain = Curtain(args.device, args.frequency_hz)
    asyncio.run(getattr(curtain, args.command)())


if __name__ == "__main__":
    main()
