import time

class Timer:
    def __init__(self, delegate, enabled=True):
        self.delegate = delegate
        self.next_time = None
        self.enabled = enabled

    async def __call__(self):
       if not self.enabled:
           return
       if self.next_time and time.time() < self.next_time:
           return
       await self.delegate()
       self.next_time = time.time() + self.delegate.delay()
