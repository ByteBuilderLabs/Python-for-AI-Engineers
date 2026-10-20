import asyncio


class FakeLLM:  # a stand-in for a real SDK that throws a 503 on the calls you pick
    def __init__(self, fail_calls=()):
        self.fail_calls, self.calls = set(fail_calls), 0

    async def complete(self, prompt):
        self.calls += 1
        await asyncio.sleep(0.05)
        if self.calls in self.fail_calls:
            raise ConnectionError(f"503 on call {self.calls}")
        return {"text": "Go with pgvector.", "tokens": 400}
