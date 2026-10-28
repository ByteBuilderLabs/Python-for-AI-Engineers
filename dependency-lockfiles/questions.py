import random
import re

rng = random.Random(42)  # fixed seed, so every build gets the same 40 questions
QUESTIONS = {}
for i in range(40):
    a, b = rng.randint(100, 999), rng.randint(10, 99)
    QUESTIONS[f"q{i:02d}"] = (f"What is {a} times {b}?", a * b)


def check(answer: str, expected: int) -> bool:
    numbers = re.findall(r"\d[\d,]*", answer)
    return bool(numbers) and int(numbers[-1].replace(",", "")) == expected
