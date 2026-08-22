import json
import random

random.seed(1337)
CURRENCIES = ["USD", "EUR", "GBP"]


def clean_record():
    return {
        "price": round(random.uniform(5, 500), 2),
        "currency": random.choice(CURRENCIES),
        "in_stock": random.choice([True, False]),
        "updated_at": "2026-08-19T14:03:00Z",
    }


def corrupt(rec, mode):
    if mode == "str_price":
        rec["price"] = f"{rec['price']:.2f}"
    elif mode == "str_bool":
        rec["in_stock"] = str(rec["in_stock"]).lower()
    elif mode == "drop_currency":
        del rec["currency"]
    elif mode == "extra_field":
        rec["discount_pct"] = 15
    else:
        rec["updated_at"] = rec["updated_at"].rstrip("Z")
    return rec


MODES = ["str_price", "str_bool", "drop_currency", "extra_field", "naive_ts"]
BAD = {i: MODES[n % 5] for n, i in enumerate(random.sample(range(300), 41))}

records, truth = [], []
for i in range(300):
    rec = clean_record()
    truth.append(dict(rec))
    if i in BAD:
        corrupt(rec, BAD[i])
    records.append(rec)

json.dump([json.dumps(r) for r in records], open("responses.json", "w"), indent=2)
json.dump(truth, open("truth.json", "w"), indent=2)
print(f"wrote {len(records)} responses, {len(BAD)} corrupted")
