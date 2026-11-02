import pytest

from agent import ORDERS

pytestmark = pytest.mark.parametrize("order_id", ORDERS)  # 30 orders x 2 tests = 60


def test_calls_lookup_tool(results, order_id):
    assert results[order_id]["tool_calls"] == [("lookup_order", {"order_id": order_id})]


def test_answer_mentions_status(results, order_id):
    assert ORDERS[order_id] in results[order_id]["answer"].lower()
