MODEL = "claude-haiku-5-5"
STATUSES = ["shipped", "processing", "delivered"]
ORDERS = {f"A-{100 + i}": STATUSES[i % 3] for i in range(30)}
TOOLS = [
    {
        "name": "lookup_order",
        "description": "Get an order's status by id, like A-100.",
        "input_schema": {
            "type": "object",
            "properties": {"order_id": {"type": "string"}},
        },
    }
]


def lookup_order(order_id):
    return ORDERS.get(order_id, "not found")


def cost_usd(usage):  # dollars per million tokens: check your model's pricing
    return (usage.input_tokens * 1.00 + usage.output_tokens * 5.00) / 1_000_000


def run_agent(client, prompt):
    messages = [{"role": "user", "content": prompt}]
    tool_calls, cost = [], 0.0
    for _ in range(5):  # hard stop, so a confused model can't loop forever
        reply = client.messages.create(
            model=MODEL, max_tokens=300, tools=TOOLS, messages=messages
        )
        cost += cost_usd(reply.usage)
        calls = [block for block in reply.content if block.type == "tool_use"]
        if not calls:
            answer = "".join(
                block.text for block in reply.content if block.type == "text"
            )
            return {"answer": answer, "tool_calls": tool_calls, "cost": cost}
        tool_calls += [(call.name, call.input) for call in calls]
        messages.append({"role": "assistant", "content": reply.content})
        messages.append(
            {
                "role": "user",
                "content": [
                    {
                        "type": "tool_result",
                        "tool_use_id": call.id,
                        "content": lookup_order(call.input.get("order_id")),
                    }
                    for call in calls
                ],
            }
        )
    raise RuntimeError("agent never finished")
