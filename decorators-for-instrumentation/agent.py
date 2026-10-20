import asyncio

from instrument import instrumented, span
from llm import FakeLLM

llm = FakeLLM(fail_calls={1, 2})


@instrumented
async def search_docs(question):  # the agent's one tool
    return {"text": "pgvector if you run Postgres, Qdrant if you need scale."}


@instrumented
async def ask_llm(prompt):
    return await llm.complete(prompt)


async def run_agent(question):
    async with span("run_agent"):
        docs = await search_docs(question)
        return await ask_llm(f"{question} Use these docs: {docs['text']}")


print(asyncio.run(run_agent("Which vector database should we use?"))["text"])
