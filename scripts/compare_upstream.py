"""Reuse Pillow #9621's matching and table rendering for experiment reports."""
from __future__ import annotations

import argparse
import datetime
import importlib.util
import json
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("artifacts", type=Path)
parser.add_argument("--pillow", type=Path, default=Path("Pillow"))
parser.add_argument("--output", type=Path, default=Path("UPSTREAM-COMPARISON.md"))
parser.add_argument("--pypi-snapshot", type=Path, default=Path("pypi-baseline.json"))
args = parser.parse_args()
spec = importlib.util.spec_from_file_location("pillow_dist_sizes", args.pillow / ".github/compare-dist-sizes.py")
upstream = importlib.util.module_from_spec(spec)
spec.loader.exec_module(upstream)
rows = {}
for path in sorted(args.artifacts.rglob("sizes.json")):
    for row in json.loads(path.read_text()):
        rows[(row["platform"], row["variant"])] = row
groups = {}
for row in rows.values():
    groups.setdefault(row["variant"], {})[upstream.key_for(row["wheel"])] = (row["wheel"], row["bytes"])
if args.pypi_snapshot.exists():
    snapshot = json.loads(args.pypi_snapshot.read_text())
    version, pypi = snapshot["version"], snapshot["sizes"]
else:
    version, pypi = upstream.fetch_pypi_sizes()
    snapshot = {"version": version, "fetched_at": datetime.datetime.now(datetime.timezone.utc).isoformat(), "sizes": pypi}
    args.pypi_snapshot.write_text(json.dumps(snapshot, indent=2) + "\n")
lines = ["# Comparisons using Pillow's own tooling", "",
         "Tables use the unmodified key matching and rendering functions from Pillow's `.github/compare-dist-sizes.py` (PR #9621), at the pinned experiment commit.", "",
         "The same-commit tables isolate JPEG XL. The PyPI tables also include unrelated changes since the release. Totals cover only the sampled wheel tags; they do not represent a complete Pillow release matrix.", ""]
for variant in ("no-jxl", "pr", "decoder", "minsize", "lto", "scalar"):
    local = groups.get(variant)
    if not local:
        continue
    lines += [f"# {variant}", ""]
    for baseline, label in ((groups.get("no-jxl", {}), "same-commit JPEG XL disabled"),
                            (groups.get("pr", {}), "same-commit original JPEG XL PR"),
                            (pypi, f"Pillow {version} on PyPI")):
        # Show the sampled platform tags; upstream's totals and missing/new-wheel
        # behavior are unchanged. Omitted release wheels would be orphan rows.
        selected = {key: value for key, value in baseline.items() if key in local}
        lines.append(upstream.render_table(label, selected, local, markdown=True))
args.output.write_text("\n".join(lines), encoding="utf-8")
print(f"Wrote {args.output}; PyPI baseline preserved in {args.pypi_snapshot}")
