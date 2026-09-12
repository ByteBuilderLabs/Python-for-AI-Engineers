import asyncio, random, statistics, threading, time
from concurrent.futures import ThreadPoolExecutor
import httpx

URL = "http://127.0.0.1:8100/work/{}"
ITEMS = range(50)
peak = [0]


def report(name, t0, lat, refused):
    wall = time.perf_counter() - t0
    p50 = statistics.median(lat) if lat else 0
    p95 = statistics.quantiles(lat, n=20)[-1] if len(lat) > 1 else 0
    print(
        f"{name:8} wall={wall:6.1f}s p50={p50:4.2f} p95={p95:4.2f} "
        f"429={refused:3} threads={peak[0]:3}"
    )
    peak[0] = 0


def call(client, i, lat, refused):
    t = time.perf_counter()
    peak[0] = max(peak[0], threading.active_count())
    if client.get(URL.format(i)).status_code == 429:
        refused.append(i)
    else:
        lat.append(time.perf_counter() - t)


def serial():
    lat, refused, t0 = [], [], time.perf_counter()
    with httpx.Client(timeout=30) as c:
        for i in ITEMS:
            call(c, i, lat, refused)
    report("serial", t0, lat, len(refused))


def threaded(workers=8):
    lat, refused, t0 = [], [], time.perf_counter()
    with httpx.Client(timeout=30) as c, ThreadPoolExecutor(workers) as pool:
        list(pool.map(lambda i: call(c, i, lat, refused), ITEMS))
    report("threads", t0, lat, len(refused))


async def one(client, i, lat, refused):
    t = time.perf_counter()
    peak[0] = max(peak[0], threading.active_count())
    r = await client.get(URL.format(i))
    if r.status_code == 429:
        refused.append(i)
    else:
        lat.append(time.perf_counter() - t)


async def gather_all():
    lat, refused, t0 = [], [], time.perf_counter()
    async with httpx.AsyncClient(timeout=30) as c:
        await asyncio.gather(*(one(c, i, lat, refused) for i in ITEMS))
    report("gather", t0, lat, len(refused))


async def guarded(client, i, sem, lat, refused):
    async with sem:
        for attempt in range(4):
            t = time.perf_counter()
            peak[0] = max(peak[0], threading.active_count())
            async with asyncio.timeout(10):
                r = await client.get(URL.format(i))
            if r.status_code != 429:
                lat.append(time.perf_counter() - t)
                return
            await asyncio.sleep(0.5 * 2**attempt + random.random() * 0.3)
        refused.append(i)


async def bounded(limit=14):
    lat, refused, t0 = [], [], time.perf_counter()
    sem = asyncio.Semaphore(limit)
    async with httpx.AsyncClient(timeout=30) as c:
        await asyncio.gather(*(guarded(c, i, sem, lat, refused) for i in ITEMS))
    report("bounded", t0, lat, len(refused))


if __name__ == "__main__":
    try:
        httpx.get("http://127.0.0.1:8100/ping", timeout=5)
    except httpx.ConnectError:
        raise SystemExit(
            "fixture not running: python -m uvicorn fixture:app --port 8100"
        )
    serial()
    threaded()
    asyncio.run(gather_all())
    asyncio.run(bounded())
