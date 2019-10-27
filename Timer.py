import time

class Timer:
    def __init__(self, delegate):
        self.delegate = delegate
        self.next_time = None

    async def __call__(self):
       if self.next_time and time.time() < self.next_time:
           return
       await self.delegate()
       self.next_time = time.time() + self.delegate.delay()
