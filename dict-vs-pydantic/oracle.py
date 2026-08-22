RATES = {"USD": 1.0, "EUR": 1.09, "GBP": 1.27}
FIELDS = {"price": float, "currency": str, "in_stock": bool, "updated_at": str}


def true_total(truth):
    return sum(r["price"] * RATES[r["currency"]] for r in truth if r["in_stock"])


def classify(rec):
    for name, kind in FIELDS.items():
        if name not in rec:
            return "missing_defaulted"
        if type(rec[name]) is not kind:
            return "wrong_type_accepted"
    if not rec["updated_at"].endswith("Z"):
        return "naive_timestamp"
    return "extra_retained" if set(rec) - set(FIELDS) else "ok"
