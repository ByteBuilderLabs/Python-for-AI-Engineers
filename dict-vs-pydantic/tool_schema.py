import json
from models import ProductRecord

tool = {
    "name": "extract_product",
    "description": "Extract product pricing from a page.",
    "input_schema": ProductRecord.model_json_schema(),
}
print(json.dumps(tool, indent=2))
