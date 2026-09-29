from common import BATCH, CORPUS, embed, open_store, read, split, track, write

paths = sorted(CORPUS.glob("*.txt"))
docs = [read(p) for p in paths]
chunks = [c for d in track(docs, len(docs), "chunk") for c in split(d)]
vecs = [v for i in range(0, len(chunks), BATCH) for v in embed(chunks[i : i + BATCH])]

write(open_store(), chunks, vecs)
print(f"\ndone: {len(vecs):,} chunks")
