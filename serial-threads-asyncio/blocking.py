import asyncio, time, httpx

URL = "http://127.0.0.1:8100/work/{}"


async def heartbeat():
    while True:
        t = time.perf_counter()
        await asyncio.sleep(0.1)
        print(f"loop late by {(time.perf_counter() - t - 0.1) * 1000:7.1f} ms")


async def main():
    hb = asyncio.create_task(heartbeat())
    await asyncio.sleep(0.3)  # let the heartbeat actually start
    with httpx.Client(timeout=30) as c:  # sync client inside a coroutine
        for i in range(3):
            c.get(URL.format(i))
    await asyncio.sleep(0.3)
    hb.cancel()


asyncio.run(main())
