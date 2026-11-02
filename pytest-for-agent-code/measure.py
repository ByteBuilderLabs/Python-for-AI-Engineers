import subprocess
import sys
import time
import xml.etree.ElementTree as ET

arm, runs = sys.argv[1], int(sys.argv[2])
outcomes, spend, start = {}, 0.0, time.perf_counter()
for i in range(1, runs + 1):
    cmd = [sys.executable, "-m", "pytest", f"--arm={arm}", "-q", "--junitxml=run.xml"]
    out = subprocess.run(cmd, capture_output=True, text=True).stdout
    spend += float(out.split("model spend: $")[1].split()[0])
    for case in ET.parse("run.xml").iter("testcase"):
        outcomes.setdefault(case.get("name"), set()).add(
            len(case) == 0
        )  # no child = passed
    flaky = sum(len(seen) == 2 for seen in outcomes.values())
    print(
        f"{arm} {i}/{runs}: {(time.perf_counter() - start) / i:.1f}s per run, ${spend / i:.2f} per run, {flaky} flaky",
        flush=True,
    )
