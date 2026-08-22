import json
from pydantic import ValidationError
from models import ProductRecord

responses = json.load(open("responses.json"))
failures = 0

for i, raw in enumerate(responses):
    try:
        ProductRecord.model_validate_json(raw)
    except ValidationError as e:
        failures += 1
        err = e.errors()[0]
        print(f"#{i:>3} {'.'.join(map(str, err['loc']))}: {err['msg']}")
print(f"{failures} of {len(responses)} rejected at the boundary")
