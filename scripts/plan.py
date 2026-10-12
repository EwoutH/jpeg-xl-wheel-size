from __future__ import annotations

import json
import os

targets = [
    dict(name="linux-x86_64", os="ubuntu-24.04", arch="x86_64", platform="linux", build="cp313-manylinux_x86_64"),
    dict(name="linux-aarch64", os="ubuntu-24.04-arm", arch="aarch64", platform="linux", build="cp313-manylinux_aarch64"),
    dict(name="macos-x86_64", os="macos-15-intel", arch="x86_64", platform="macos", build="cp313-macosx_x86_64"),
    dict(name="macos-arm64", os="macos-15", arch="arm64", platform="macos", build="cp313-macosx_arm64"),
    dict(name="windows-amd64", os="windows-2022", arch="AMD64", platform="windows", build="cp313-win_amd64"),
]
selected = os.environ.get("SELECTED", "all").split(",")
assert "all" in selected or set(selected) <= {t["name"] for t in targets}, selected
targets = [t for t in targets if "all" in selected or t["name"] in selected]
print("targets=" + json.dumps(targets))
