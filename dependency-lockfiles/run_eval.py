import json, os
from importlib.metadata import distributions
from agent import ask
from questions import QUESTIONS, check

build = os.environ["BUILD"]
packages = {d.metadata["Name"]: d.version for d in distributions()}
answers = {qid: ask(question) for qid, (question, _) in QUESTIONS.items()}
passed = {
    qid: check(answers[qid], expected) for qid, (_, expected) in QUESTIONS.items()
}

with open(f"/out/{build}.json", "w", encoding="utf-8") as f:
    json.dump({"packages": packages, "answers": answers, "passed": passed}, f, indent=2)
print(f"{build}: {sum(passed.values())}/40 passed, {len(packages)} packages installed")
