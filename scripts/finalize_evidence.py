"""Archive final CI metadata and validate the complete experiment matrix."""
from pathlib import Path
import argparse
import json
import shutil
import xml.etree.ElementTree as ET

repo = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument("--report", type=Path, default=repo / "artifacts/final-report-complete")
args = parser.parse_args()
source = args.report
out = repo / "evidence"
shutil.copytree(source / "measurements", out / "raw", dirs_exist_ok=True)
for name in ("RESULTS.md", "UPSTREAM-COMPARISON.md", "pypi-baseline.json"):
    dest = out / "reports" / name
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source / name, dest)
platforms = ("linux-x86_64", "linux-aarch64", "macos-x86_64", "macos-arm64", "windows-amd64")
variants = ("no-jxl", "pr", "decoder", "minsize", "lto", "scalar")
rows, checks, provenance, test_provenance = {}, {}, {}, {}

def completed_job(path, stage, platform, variant):
    run = json.loads((path.parents[1] / "run.json").read_text())
    suffix = f" / {stage} {variant} ({platform})"
    jobs = [job for job in run["jobs"] if job["name"].endswith(suffix)]
    assert len(jobs) == 1 and jobs[0]["conclusion"] == "success", (path, suffix, jobs)
    return {"run": run["databaseId"], "job_url": jobs[0]["url"]}

for path in sorted((out / "raw").rglob("sizes.json")):
    for row in json.loads(path.read_text()):
        rows[(row["platform"], row["variant"])] = row
        provenance[(row["platform"], row["variant"])] = completed_job(path, "Build", row["platform"], row["variant"])
        assert sum(m["installed"] for m in row["members"]) == row["installed_bytes"]
for path in sorted((out / "raw").rglob("verification.json")):
    result = json.loads(path.read_text())
    key = (result["platform"], result["variant"])
    assert result["jpegxl"] == (key[1] != "no-jxl")
    root = ET.parse(path.with_name("tests.xml")).getroot()
    suites = [root] if root.tag == "testsuite" else list(root.findall("testsuite"))
    counts = {k: sum(int(s.get(k, 0)) for s in suites) for k in ("tests", "failures", "errors", "skipped")}
    assert counts["tests"] == 196 and counts["errors"] == counts["failures"] == 0
    checks[key] = counts
    test_provenance[key] = completed_job(path, "Test", *key)
expected = {(p, v) for p in platforms for v in variants}
assert rows.keys() == checks.keys() == expected, (expected - rows.keys(), expected - checks.keys())
summary = {"pillow_commit": "d00ba3a89faabd31fd92c3b506c86557da8c0a0b", "platforms": {}}
for platform in platforms:
    base, pr = rows[(platform, "no-jxl")], rows[(platform, "pr")]
    items = {}
    for variant in variants:
        row = rows[(platform, variant)]
        items[variant] = {k: v for k, v in row.items() if k != "members"}
        items[variant].update(
            build=provenance[(platform, variant)],
            test_job=test_provenance[(platform, variant)],
            added_bytes=row["bytes"] - base["bytes"],
            growth_percent=100 * (row["bytes"] / base["bytes"] - 1),
            added_installed_bytes=row["installed_bytes"] - base["installed_bytes"],
            overhead_removed_percent=100 * (1 - (row["bytes"] - base["bytes"]) / (pr["bytes"] - base["bytes"])),
            tests=checks[(platform, variant)],
        )
    src = repo / "artifacts" / ("controlled-" + platform)
    shutil.copytree(src, out / "controlled" / platform, dirs_exist_ok=True)
    controlled = json.loads((src / "comparison.json").read_text())
    assert len(controlled["comparisons"]) == 30
    summary["platforms"][platform] = items
totals = {k: sum(row[k] for row in checks.values()) for k in ("tests", "failures", "errors", "skipped")}
totals["passed"] = totals["tests"] - totals["skipped"] - totals["failures"] - totals["errors"]
summary["pytest_totals"] = totals
(out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
print("Validated 30 wheel measurements, 30 test results, 5 same-host comparisons:", totals)
for platform in platforms:
    items = summary["platforms"][platform]
    print(platform, "overhead removed:", {v: round(items[v]["overhead_removed_percent"], 2) for v in ("decoder", "lto")})
    for variant in ("pr", "decoder", "lto"):
        libs = [m for m in rows[(platform, variant)]["members"] if "jxl" in m["name"].lower() or "jpegxl" in m["name"].lower()]
        print(variant, [(m["name"], m["installed"]) for m in libs])
