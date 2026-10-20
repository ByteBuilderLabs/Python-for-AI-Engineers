import asyncio

from blog_retry import retry
from llm import FakeLLM

llm = FakeLLM(fail_calls={1, 2})


@retry
async def ask_llm(prompt):
    return await llm.complete(prompt)


print("sync check passes:", bool(ask_llm("hi")))
asyncio.run(ask_llm("hi"))  # a working retry would survive calls 1 and 2
