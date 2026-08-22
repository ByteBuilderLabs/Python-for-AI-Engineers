import json
from oracle import RATES, true_total

responses = json.load(open("responses.json"))
truth = json.load(open("truth.json"))
total = 0.0

for raw in responses:
    try:
        rec = json.loads(raw)
        if rec.get("in_stock", False):
            total += rec["price"] * RATES.get(rec.get("currency", "USD"), 1.0)
    except Exception:
        continue


real = true_total(truth)
print(f"pipeline total  ${total:,.2f}")
print(f"ground truth    ${real:,.2f}")
print(f"delta           {(total - real) / real:+.1%}")
