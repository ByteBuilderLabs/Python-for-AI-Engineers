import asyncio
import functools
from contextlib import asynccontextmanager


def instrumented(fn):
    # @functools.wraps(fn)
    async def wrapper(*args):
        for attempt in range(3):
            try:
                return record(fn.__name__, attempt, await fn(*args))
            except ConnectionError:
                # if attempt == 2:
                #     raise
                await asyncio.sleep(0.2 * 2**attempt)

    return wrapper


CALLS = []  # every instrumented call lands here, so a span can add them up


def record(name, retries, result):  # illustrative price: $15 per million tokens
    cost = result.get("tokens", 0) * 15e-6
    CALLS.append({"fn": name, "retries": retries, "cost": cost})
    print(f"{name}: retries={retries} cost=${cost:.4f}")
    return result


@asynccontextmanager
async def span(name):
    first = len(CALLS)
    yield
    step = CALLS[first:]
    retries, cost = sum(c["retries"] for c in step), sum(c["cost"] for c in step)
    print(f"{name}: {len(step)} calls, {retries} retries, ${cost:.4f} total")
