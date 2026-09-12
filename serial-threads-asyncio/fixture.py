from fastapi import FastAPI, HTTPException
import asyncio, time

app = FastAPI()
BURST, REFILL = 40.0, 8.0
tokens, last = BURST, time.monotonic()


def take_token():
    global tokens, last
    now = time.monotonic()
    tokens = min(BURST, tokens + (now - last) * REFILL)
    last = now
    if tokens < 1:
        raise HTTPException(429, "slow down")
    tokens -= 1


BASE, KNEE, STEP = 1.8, 16, 0.12
inflight = 0


@app.get("/work/{item_id}")
async def work(item_id: int):
    global inflight
    take_token()
    inflight += 1
    try:
        await asyncio.sleep(BASE + STEP * max(0, inflight - KNEE))
    finally:
        inflight -= 1
    return {"item": item_id}


@app.get("/ping")
def ping():
    return {"ok": True}
