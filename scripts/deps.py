"""Archive installed dependency prefixes, not huge compiler/source build trees."""
from __future__ import annotations

import argparse
import hashlib
import json
import tarfile
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("operation", choices=("save", "restore"))
parser.add_argument("prefix", type=Path)
parser.add_argument("--windows", action="store_true")
args = parser.parse_args()
root = Path(__file__).resolve().parents[1]
bundle = root / "dependency-bundle"
bundle.mkdir(exist_ok=True)
archive = bundle / "deps.tar"
manifest = bundle / "manifest.json"
prefix = args.prefix.resolve()
if args.operation == "save":
    names = ("inc", "lib", "bin", "license") if args.windows else ("include", "lib", "lib64", "bin", "share")
    with tarfile.open(archive, "w") as tar:
        for name in names:
            path = prefix / name
            if path.exists():
                tar.add(path, arcname=name)
    manifest.write_text(json.dumps({"prefix": str(prefix), "sha256": hashlib.file_digest(archive.open("rb"), "sha256").hexdigest()}, indent=2))
else:
    info = json.loads(manifest.read_text())
    assert info["sha256"] == hashlib.file_digest(archive.open("rb"), "sha256").hexdigest(), "Dependency archive checksum mismatch"
    # Shared libraries have absolute install names; never restore to another prefix.
    assert info["prefix"] == str(prefix), (info["prefix"], str(prefix))
    prefix.mkdir(parents=True, exist_ok=True)
    with tarfile.open(archive) as tar:
        # Trusted artifact from this workflow; preserve absolute symlinks used by
        # native tool installations, while checking all archive member paths.
        for member in tar.getmembers():
            assert not member.name.startswith("/") and ".." not in Path(member.name).parts
        tar.extractall(prefix, filter="fully_trusted")
print(f"{args.operation}: {archive.stat().st_size / 1048576:.1f} MiB dependency bundle at {prefix}")
