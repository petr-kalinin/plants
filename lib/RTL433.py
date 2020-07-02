import asyncio
import json
import time

MAX_UPDATE_DELAY = 10 * 60
INITIAL_UPDATE_DELAY = 60

class RTL433:
    def __init__(self):
        self._process = None
        self._temperature = None
        self._humidity = None
        self._last_update_time = time.time() - MAX_UPDATE_DELAY + INITIAL_UPDATE_DELAY

    async def update(self):
        if self._last_update_time and time.time() > self._last_update_time + MAX_UPDATE_DELAY:
            self._temperature = None
            self._humidity = None
            print("Kill RTL433 process!")
            if self._process:
                self._process.kill()
            self._process = None
            self._last_update_time = time.time()
        if not self._process or self._process.returncode is not None:
            self._process = await asyncio.create_subprocess_exec(
                'rtl_433', '-F', 'json', '-g', '19.2', stdout=asyncio.subprocess.PIPE)
        try:
            while True:
                line = await asyncio.wait_for(self._process.stdout.readline(), timeout=2)
                print("RTL433 received line", line)
                print("Process return code", self._process.returncode)
                data = json.loads(line)
                if data["model"] != "Prologue-TH":
                    continue
                self._temperature = data["temperature_C"]
                self._humidity = data["humidity"]
                self._last_update_time = time.time()
        except asyncio.TimeoutError:
            pass
        except Exception as e:
            print("Error in update: ", e)
            pass

    def temperature(self):
        return self._temperature

    def humidity(self):
        return self._humidity


async def main():
    rtl433 = RTL433()
    while True:
        await rtl433.update()
        print(rtl433.temperature(), rtl433.humidity())
        await asyncio.sleep(0.3)

if __name__ == "__main__":
    asyncio.run(main())
