from langchain.agents import create_agent
from langchain_openai import ChatOpenAI


def multiply(a: int, b: int) -> int:
    """Multiply two whole numbers."""
    return a * b


agent = create_agent(
    model=ChatOpenAI(model="gpt-4.1-mini", temperature=0),
    tools=[multiply],
    system_prompt="Use the multiply tool, then reply with the final number only.",
)


def ask(question: str) -> str:
    return agent.invoke({"messages": [{"role": "user", "content": question}]})[
        "messages"
    ][-1].content
