"""Summarize downloaded experiment artifacts and compare identical wheel members."""
from __future__ import annotations

import argparse
import json
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path


def repack(source: Path, output: Path) -> dict:
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(source) as original, zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as packed:
        for member in original.infolist():
            packed.writestr(member, original.read(member), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    with zipfile.ZipFile(source) as original, zipfile.ZipFile(output) as packed:
        assert original.namelist() == packed.namelist()
        assert all(original.read(n) == packed.read(n) for n in original.namelist())
    return {"original_bytes": source.stat().st_size, "level9_bytes": output.stat().st_size,
            "saved_bytes": source.stat().st_size - output.stat().st_size}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("artifacts", type=Path)
    parser.add_argument("--output", type=Path, default=Path("RESULTS.md"))
    parser.add_argument("--repack", action="store_true")
    args = parser.parse_args()
    rows = []
    wheel_paths = {}
    for path in sorted(args.artifacts.rglob("sizes.json")):
        current = json.loads(path.read_text())
        rows.extend(current)
        for row in current:
            wheel_paths[(row["platform"], row["variant"])] = path.parent / "wheelhouse" / row["wheel"]
    rows = list({(row["platform"], row["variant"]): row for row in rows}.values())
    assert rows, "No measurements found"
    order = {name: index for index, name in enumerate(("no-jxl", "pr", "decoder", "minsize", "lto", "scalar"))}
    rows.sort(key=lambda row: (row["platform"], order[row["variant"]]))
    lookup = {(row["platform"], row["variant"]): row for row in rows}
    lines = ["# Measured wheel sizes", "", "Sizes are MiB (1,048,576 bytes). Comparisons use the same Pillow commit and CPython ABI.", "", "| Platform | Variant | Wheel MiB | Installed MiB | vs PR | JPEG XL overhead vs disabled |", "| --- | --- | ---: | ---: | ---: | ---: |"]
    for row in rows:
        pr = lookup.get((row["platform"], "pr"))
        base = lookup.get((row["platform"], "no-jxl"))
        change = f'{100 * (row["bytes"] / pr["bytes"] - 1):+.2f}%' if pr else "pending"
        overhead = f'{(row["bytes"] - base["bytes"]) / 1048576:+.3f} MiB ({100 * (row["bytes"] / base["bytes"] - 1):+.2f}%)' if base else "pending"
        lines.append(f'| {row["platform"]} | {row["variant"]} | {row["bytes"] / 1048576:.3f} | {row["installed_bytes"] / 1048576:.3f} | {change} | {overhead} |')
    lines += ["", "## Decoding checks", "", "The workflow asserts JPEG XL availability and runs selftest plus the JPEG XL, JPEG and PNG tests. Pixel hashes below compare each variant against PR on the same architecture. A hash difference needs investigation; matching hashes cover these samples only.", ""]
    verification = {}
    for path in sorted(args.artifacts.rglob("verification.json")):
        result = json.loads(path.read_text())
        if result.get("platform"):
            verification[(result["platform"], result["variant"])] = result
            continue
        parent = next((p for p in path.parents if (p / "sizes.json").exists()), None)
        if parent:
            row = json.loads((parent / "sizes.json").read_text())[0]
            verification[(row["platform"], row["variant"])] = json.loads(path.read_text())
    for row in rows:
        key = (row["platform"], row["variant"])
        result, baseline = verification.get(key), verification.get((row["platform"], "pr"))
        if not result or not result["jpegxl"] or not baseline:
            continue
        hashes = {f["name"]: (f["mode"], f["size"], f["sha256"]) for f in baseline["files"]}
        differences = [f["name"] for f in result["files"] if hashes.get(f["name"]) != (f["mode"], f["size"], f["sha256"])]
        equal = not differences and len(hashes) == len(result["files"])
        baseline_time = sum(f["median_seconds"] for f in baseline["files"])
        ratio = sum(f["median_seconds"] for f in result["files"]) / baseline_time
        lines.append(f'- {key[0]} / {key[1]}: pixel hashes {"match" if equal else "DIFFER"}; sum of sample median decode times {ratio:.2f}× PR.')
        if differences:
            lines.append(f'  Differing samples: {", ".join(differences)}.')
    lines += ["", "Hosted runners differ: timing ratios are exploratory, not controlled performance benchmarks."]
    lines += ["", "## Saved pytest results", "", "Counts include optional-dependency skips. Availability assertions and Pillow selftest are separate workflow steps.", "", "| Artifact | Tests | Failures | Errors | Skipped |", "| --- | ---: | ---: | ---: | ---: |"]
    test_paths = {}
    for path in sorted(args.artifacts.rglob("tests.xml")):
        check = path.with_name("verification.json")
        result = json.loads(check.read_text()) if check.exists() else {}
        key = (result.get("platform", path.parent.name), result.get("variant", "unknown"))
        test_paths[key] = path
    for key, path in sorted(test_paths.items()):
        root = ET.parse(path).getroot()
        suites = [root] if root.tag == "testsuite" else list(root.findall("testsuite"))
        counts = [sum(int(s.get(key, 0)) for s in suites) for key in ("tests", "failures", "errors", "skipped")]
        lines.append(f'| {path.parent.name} | ' + " | ".join(map(str, counts)) + " |")
    if args.repack:
        lines += ["", "## ZIP compression level 9", "", "Repacked wheel contents are byte-for-byte identical, including RECORD. Installed size is unchanged.", "", "| Wheel | Saved KiB | Saved % |", "| --- | ---: | ---: |"]
        for key, path in sorted(wheel_paths.items()):
            if not path.exists():
                continue
            result = repack(path, path.parent / "repacked" / path.name)
            lines.append(f'| {path.relative_to(args.artifacts)} | {result["saved_bytes"] / 1024:.1f} | {100 * result["saved_bytes"] / result["original_bytes"]:.2f}% |')
    args.output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
