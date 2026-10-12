"""Fail if JPEG XL disappeared; record pixels and a small warm decode benchmark."""
from __future__ import annotations

import hashlib
import json
import os
import statistics
import time
from pathlib import Path

from PIL import Image, features

root = Path(__file__).resolve().parents[1]
variant = Path(__file__).with_name("variant.txt").read_text().strip()
enabled = features.check_module("jpegxl")
assert enabled == (variant != "no-jxl"), (variant, enabled)
results = {"variant": variant, "platform": os.environ.get("EXPERIMENT_PLATFORM"), "jpegxl": enabled, "files": []}
if enabled:
    for name in ("hopper.jxl", "hopper_gray.jxl", "transparent.jxl", "flower.jxl", "flower2.jxl", "16bit_subcutaneous.cropped.jxl"):
        path = root / "Tests/images/jxl" / name
        def decode():
            with Image.open(path) as image:
                image.load()
                return image.mode, image.size, hashlib.sha256(image.tobytes()).hexdigest()
        mode, size, digest = decode()
        samples = []
        for _ in range(9):
            start = time.perf_counter()
            for _ in range(10):
                with Image.open(path) as image:
                    image.load()
            samples.append((time.perf_counter() - start) / 10)
        results["files"].append({"name": name, "mode": mode, "size": size,
                                 "sha256": digest, "median_seconds": statistics.median(samples)})
output = root / "size_experiment/verification.json"
output.write_text(json.dumps(results, indent=2) + "\n")
print(output.read_text())
