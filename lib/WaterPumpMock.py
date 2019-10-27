import logging

class WaterPump:
    async def start(self):
        logging.info("Water pump started")

    async def stop(self):
        logging.info("Water pump stopped")