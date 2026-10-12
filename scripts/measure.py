"""Inspect real wheel ZIPs, including uncompressed and per-member size."""
from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("wheelhouse", type=Path)
parser.add_argument("output", type=Path)
parser.add_argument("--variant", required=True)
parser.add_argument("--platform", required=True)
args = parser.parse_args()
rows = []
for path in sorted(args.wheelhouse.glob("*.whl")):
    with zipfile.ZipFile(path) as wheel:
        members = [{"name": i.filename, "compressed": i.compress_size, "installed": i.file_size}
                   for i in wheel.infolist() if not i.is_dir()]
    rows.append({"wheel": path.name, "variant": args.variant, "platform": args.platform,
                 "bytes": path.stat().st_size, "installed_bytes": sum(i["installed"] for i in members),
                 "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                 "members": sorted(members, key=lambda i: i["installed"], reverse=True)})
assert len(rows) == 1, f"Expected exactly one wheel, found {len(rows)}"
args.output.write_text(json.dumps(rows, indent=2) + "\n")
print(json.dumps([{k: v for k, v in row.items() if k != "members"} for row in rows], indent=2))
