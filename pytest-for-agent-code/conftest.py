import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from types import SimpleNamespace

import httpx2
import pytest
from anthropic import Anthropic, DefaultHttpxClient
from anthropic.types import Message
from agent import ORDERS, cost_usd, run_agent


def pytest_addoption(parser):
    parser.addoption("--arm", choices=["live", "recorded", "unit"], default="recorded")
    parser.addoption("--record", action="store_true")


SPEND = []  # dollars, one entry per real response


def live_client(save_to=None):
    bodies = []

    def keep(response):  # runs on every real HTTP response
        if response.status_code == 200:
            bodies.append(json.loads(response.read()))
            SPEND.append(cost_usd(SimpleNamespace(**bodies[-1]["usage"])))
            if save_to:
                save_to.write_text(json.dumps(bodies, indent=2))

    return Anthropic(
        timeout=30.0, http_client=DefaultHttpxClient(event_hooks={"response": [keep]})
    )


def replay_client(bodies):
    queue = iter(bodies)
    transport = httpx2.MockTransport(
        lambda request: httpx2.Response(200, json=next(queue))
    )
    return Anthropic(
        api_key="test-key", http_client=DefaultHttpxClient(transport=transport)
    )


def fake_client(bodies):
    queue = iter(bodies)
    create = lambda **kwargs: Message.model_validate(next(queue))
    return SimpleNamespace(messages=SimpleNamespace(create=create))


def client_for(order_id, arm, record):
    path = Path(__file__).parent / "cassettes" / f"{order_id}.json"
    if arm == "live" or (record and not path.exists()):
        return live_client(save_to=None if arm == "live" else path)
    return (fake_client if arm == "unit" else replay_client)(
        json.loads(path.read_text())
    )


@pytest.fixture(scope="session")
def results(request):
    arm, record = request.config.getoption("--arm"), request.config.getoption(
        "--record"
    )

    def ask(order_id):
        try:
            return run_agent(
                client_for(order_id, arm, record), f"Where is order {order_id}?"
            )
        except (
            Exception
        ) as error:  # a failed API call fails its own tests, not the whole run
            return {"answer": repr(error), "tool_calls": [], "cost": 0.0}

    with ThreadPoolExecutor(max_workers=5) as pool:
        return dict(zip(ORDERS, pool.map(ask, ORDERS)))


def pytest_terminal_summary(terminalreporter):
    terminalreporter.write_line(f"model spend: ${sum(SPEND):.2f}")
