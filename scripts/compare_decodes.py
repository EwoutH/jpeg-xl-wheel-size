"""Compare saved wheels on one runner, without rebuilding native libraries."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import statistics
import subprocess
import sys
import time

parser = argparse.ArgumentParser()
parser.add_argument("artifacts", type=Path)
parser.add_argument("images", type=Path)
parser.add_argument("--worker", type=Path)
args = parser.parse_args()
names = ("hopper.jxl", "hopper_gray.jxl", "transparent.jxl", "flower.jxl", "flower2.jxl", "16bit_subcutaneous.cropped.jxl")
if args.worker:
    import numpy as np
    from PIL import Image, features

    assert features.check_module("jpegxl")
    args.worker.mkdir(parents=True, exist_ok=True)
    rows = []
    for name in names:
        path = args.images / name
        with Image.open(path) as im:
            im.load()
            mode, size = im.mode, im.size
            pixels = np.asarray(im).copy()
            digest = hashlib.sha256(im.tobytes()).hexdigest()
        np.save(args.worker / (name + ".npy"), pixels)
        samples = []
        for _ in range(11):
            start = time.perf_counter()
            for _ in range(10):
                with Image.open(path) as im:
                    im.load()
            samples.append((time.perf_counter() - start) / 10)
        rows.append(dict(name=name, mode=mode, size=size, sha256=digest, seconds=statistics.median(samples)))
    (args.worker / "samples.json").write_text(json.dumps(rows, indent=2))
    sys.exit()

import numpy as np

output = Path("controlled-results").resolve()
output.mkdir(exist_ok=True)
variants = ("pr", "decoder", "minsize", "lto", "scalar")
results = {}
for variant in variants:
    wheels = list(args.artifacts.glob(f"wheel-*-{variant}/wheelhouse/*.whl"))
    assert len(wheels) == 1, (variant, wheels)
    install = output / "packages" / variant
    subprocess.run([sys.executable, "-m", "pip", "install", "--no-deps", "--target", str(install), str(wheels[0])], check=True)
    env = dict(os.environ, PYTHONPATH=str(install))
    target = output / variant
    subprocess.run([sys.executable, str(Path(__file__).resolve()), str(args.artifacts.resolve()), str(args.images.resolve()), "--worker", str(target)], env=env, cwd=output, check=True)
    results[variant] = json.loads((target / "samples.json").read_text())

lines = ["# Same-runner decoding comparison", "", f"Host: `{platform.platform()}` / `{platform.processor()}`", "", "All wheels run sequentially on the same host in separate Python processes. This removes cross-runner CPU differences, but does not control thermals or shared-host load. Timing ratios are sample medians, not release performance guarantees.", "", "| Variant | Sample | Maximum channel difference | Changed channel values | Decode time vs PR |", "| --- | --- | ---: | ---: | ---: |"]
comparisons = []
for variant in variants:
    for baseline, row in zip(results["pr"], results[variant], strict=True):
        assert (baseline["name"], baseline["mode"], baseline["size"]) == (row["name"], row["mode"], row["size"])
        name = row["name"]
        a = np.load(output / "pr" / (name + ".npy")).astype(np.float64)
        b = np.load(output / variant / (name + ".npy")).astype(np.float64)
        delta = np.abs(a - b)
        maximum, changed = float(delta.max()), int(np.count_nonzero(delta))
        ratio = row["seconds"] / baseline["seconds"]
        comparisons.append(dict(variant=variant, sample=name, maximum=maximum, changed=changed, channels=int(delta.size), time_ratio=ratio))
        lines.append(f"| {variant} | {name} | {maximum:g} | {changed}/{delta.size} | {ratio:.2f} |")
(output / "comparison.json").write_text(json.dumps(dict(host=platform.uname()._asdict(), comparisons=comparisons), indent=2))
(output / "COMPARISON.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
print("\n".join(lines))
