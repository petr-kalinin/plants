import asyncio

class SHT20():
    async def humidity(self):
        await asyncio.sleep(0.1)
        return 60

    async def temperature(self):
        await asyncio.sleep(0.2)
        return 25

if __name__ == "__main__":
    sht20 = SHT20()
    print(sht20.temperature(), sht20.humidity())
