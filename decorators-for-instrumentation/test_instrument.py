import asyncio
import pytest
from instrument import instrumented
from llm import FakeLLM


@instrumented
async def ask_llm(llm):
    return await llm.complete("hi")


def test_retries_then_succeeds():
    assert asyncio.run(ask_llm(FakeLLM(fail_calls={1, 2})))["tokens"] == 400
    assert ask_llm.__name__ == "ask_llm"


def test_gives_up_after_three_tries():
    pytest.raises(ConnectionError, asyncio.run, ask_llm(FakeLLM(fail_calls={1, 2, 3})))
