import random
from pathlib import Path

rng = random.Random(42)  # fixed seed: same corpus on every machine
words = ["agent", "vector", "token", "chunk", "embed", "store", "query", "model"]
paras = [" ".join(rng.choices(words, k=90)) + ".\n" for _ in range(500)]

out = Path("corpus")
out.mkdir(exist_ok=True)
total = 0
for i in range(1200):
    text = "".join(rng.choices(paras, k=1800))  # ~1 MB per file
    (out / f"doc_{i:04d}.txt").write_text(text, encoding="utf-8", newline="\n")
    total += len(text)
print(f"wrote 1,200 files, {total / 1e9:.2f} GB")
