import json
from pathlib import Path


def load(build):
    return json.loads(Path(f"out/{build}.json").read_text(encoding="utf-8"))


direct = set(Path("requirements.txt").read_text().split())
for s in ["unpinned", "compat", "locked"]:
    old, new = load(f"{s}-old"), load(f"{s}-new")
    names = sorted(old["packages"].keys() | new["packages"].keys())
    moved = [n for n in names if old["packages"].get(n) != new["packages"].get(n)]
    changed = [q for q in old["passed"] if old["passed"][q] != new["passed"][q]]
    print(
        f"\n{s}: {len(moved)} packages moved, {len(set(moved) - direct)} transitive, {len(changed)}/40 answers changed"
    )
    for n in moved:
        print(f"   {n}: {old['packages'].get(n, '-')} -> {new['packages'].get(n, '-')}")
