from common import CORPUS
from pipeline_gen import chunk_docs, read_docs

paths = sorted(CORPUS.glob("*.txt"))[:3]

chunks = chunk_docs(read_docs(paths))
print("first pass: ", sum(1 for _ in chunks))
print("second pass:", sum(1 for _ in chunks))

try:
    print(len(chunk_docs(read_docs(paths))))
except TypeError as err:
    print("len():", err)
