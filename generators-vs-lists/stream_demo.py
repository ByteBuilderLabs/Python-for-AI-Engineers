import asyncio, time
from anthropic import AsyncAnthropic

client = AsyncAnthropic()  # reads ANTHROPIC_API_KEY from the environment


async def tokens(prompt):
    async with client.messages.stream(
        model="claude-haiku-4-5-20251001",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}],
    ) as stream:
        async for text in stream.text_stream:
            yield text


async def main():
    start, first = time.perf_counter(), None
    async for text in tokens("Explain Python generators in about 200 words."):
        if first is None:
            first = time.perf_counter() - start
        print(text, end="", flush=True)
    total = time.perf_counter() - start
    print(f"\n\ntime to first token: {first:.2f}s | full response: {total:.2f}s")


asyncio.run(main())
