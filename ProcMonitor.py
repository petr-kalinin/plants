import asyncio
import psutil
import subprocess
import os


class ProcMonitor:
    def __init__(self, graphite):
        self.graphite = graphite

    async def __call__(self):
        try:
            env = os.environ.copy()
            env["DISPLAY"] = ":0"
            name = psutil.Process(int(subprocess.check_output(["xdotool", "getactivewindow", "getwindowpid"], env=env).decode("utf-8").strip())).name()
        except:
            name = "unknown"
        await self.graphite.send('procname.' + name, 1)

    def delay(self):
        return self.graphite.delay()
