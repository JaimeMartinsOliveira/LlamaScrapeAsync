import sys
import asyncio

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())


loop = asyncio.get_event_loop()
print("Loop usado:", type(loop))