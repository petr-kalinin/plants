import asyncio
import logging
import psutil
import subprocess
import os
from urllib.parse import urlparse


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
        if name == "firefox":
            await self.send_tab("firefox")
        elif name == "yandex_browser":
            await self.send_tab("chrome/chromium")

    async def send_tab(self, browser):
        url = self.get_tab(browser)
        logging.info("Current url: {}".format(url))
        tab = self.get_domain(url)
        await self.graphite.send('tab.' + tab, 1)

    def get_tab(self, browser):
        active_list = subprocess.check_output(["/home/petr/.local/bin/bt", "active"]).decode("utf-8").strip().split("\n")
        active_id = None
        for active_tab in active_list:
            data = active_tab.split("\t")
            if data[-1].strip() == browser:
                active_id = data[0].strip()
        all_list = subprocess.check_output(["/home/petr/.local/bin/bt", "list"]).decode("utf-8").strip().split("\n")
        for tab in all_list:
           data = tab.split("\t")
           if data[0] == active_id:
               return data[-1]
        return "unknown"

    def get_domain(self, url):
        return urlparse(url).netloc.replace(".", "_")

    def delay(self):
        return self.graphite.delay()
