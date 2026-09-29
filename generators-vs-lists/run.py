import resource, subprocess, sys, time
from common import open_store

start = time.perf_counter()
proc = subprocess.run([sys.executable, sys.argv[1]])
elapsed = time.perf_counter() - start

peak = (
    resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss / 1024
)  # KB -> MB on Linux
code = 128 - proc.returncode if proc.returncode < 0 else proc.returncode
rows = open_store().execute("SELECT COUNT(*) FROM vecs").fetchone()[0]

print(f"\nexit code: {code}\npeak RSS:  {peak:,.0f} MB")
print(f"wall time: {elapsed:.1f} s\nrows written: {rows:,}")
