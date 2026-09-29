from itertools import islice
from common import BATCH, CORPUS, embed, open_store, read, split, track, write


def read_docs(paths):
    for p in paths:
        yield read(p)


def chunk_docs(docs):
    for d in docs:
        yield from split(d)


def batches(items, size):
    items = iter(items)  # islice on a list restarts at 0 on every call
    while batch := list(islice(items, size)):
        yield batch


if __name__ == "__main__":
    paths = sorted(CORPUS.glob("*.txt"))
    docs = track(read_docs(paths), len(paths), "chunk")
    db, done = open_store(), 0
    for batch in batches(chunk_docs(docs), BATCH):
        write(db, batch, embed(batch))
        done += len(batch)
    print(f"\ndone: {done:,} chunks")
