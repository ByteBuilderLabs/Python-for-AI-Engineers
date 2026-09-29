import hashlib, sqlite3
from pathlib import Path

CORPUS = Path("corpus")
CHUNK, OVERLAP, BATCH = 1000, 200, 256


def read(path):
    return path.read_text(encoding="utf-8")


def split(text):
    return [text[i : i + CHUNK] for i in range(0, len(text), CHUNK - OVERLAP)]


def embed(batch):  # stand-in for a real model: 1,536 bytes = 384 float32 dims
    return [hashlib.shake_128(c.encode()).digest(1536) for c in batch]


def open_store():
    db = sqlite3.connect("/tmp/store.db")
    db.execute("CREATE TABLE IF NOT EXISTS vecs (chunk TEXT, vec BLOB)")
    return db


def write(db, chunks, vecs):
    db.executemany("INSERT INTO vecs VALUES (?, ?)", zip(chunks, vecs))
    db.commit()


def track(items, total, label):
    for n, item in enumerate(items, 1):
        print(f"\r{label}: {n}/{total} ({n * 100 // total}%)", end="", flush=True)
        yield item
