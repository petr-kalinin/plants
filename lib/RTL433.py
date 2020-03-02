import asyncio
import json

class RTL433:
    def __init__(self):
        self._process = None
        self._temperature = None
        self._humidity = None

    async def update(self):
        if not self._process:
            self._process = await asyncio.create_subprocess_exec(
                'rtl_433', '-F', 'json', stdout=asyncio.subprocess.PIPE)
        try:
            while True:
                line = await asyncio.wait_for(self._process.stdout.readline(), timeout=2)
                data = json.loads(line)
                print("RTL433 received data", data)
                if data["model"] != "TFA-TwinPlus":
                    continue
                self._temperature = data["temperature_C"]
                self._humidity = data["humidity"]
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
