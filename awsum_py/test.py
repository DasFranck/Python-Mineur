import asyncio
import time
import signal
from datetime import datetime
import sys

URLS = ["https://dasfranck.fr/", "https://google.fr/"]
TIME = [2, 5]

begin = datetime.now()

async def print_it(name, timeout):
    while True:
        print("Sleep on %s at %d seconds" % (name, (datetime.now() - begin).seconds))
        await asyncio.sleep(timeout)
        print("Awake on %s at %d seconds" % (name, (datetime.now() - begin).seconds))

def signal_handler(signal, frame):
    loop.stop()
    sys.exit(-33)

signal.signal(signal.SIGINT, signal_handler)

for i in range(len(URLS)):
    asyncio.async(print_it(URLS[i], TIME[i]))
    print("URL %s Added" % URLS[i])

loop = asyncio.get_event_loop()
loop.run_forever()
