"""Local checks for recipe partitioning and dependency archive integrity."""
from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from prepare import VARIANTS, prepare

repo = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix="jxl-pipeline-") as temp:
    root = Path(temp)
    for variant in VARIANTS:
        for stage in ("common", "variant"):
            tree = root / f"{variant}-{stage}"
            for name in ("setup.py", ".github/workflows/wheels-dependencies.sh", "winbuild/build_prepare.py"):
                dest = tree / name
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(repo / "Pillow" / name, dest)
            prepare(tree, variant)
            subprocess.run([sys.executable, str(repo / "scripts/stage.py"), str(tree), stage], check=True)
            native = (tree / ".github/workflows/wheels-dependencies.sh").read_text()
            body = native.split("function build {\n", 1)[1].split("\nfunction create_meson_cross_config", 1)[0]
            if stage == "common":
                assert "build_jpegxl" not in body
            else:
                assert body.strip() == "install_rsync\n    build_jpegxl\n}"
                assert "pillow-depends/archive/main.zip" not in native
                assert "deps.py\" restore" in native
                assert "-DHWY_ENABLE_TESTS=OFF" in native
            compile((tree / "setup.py").read_text(), "setup.py", "exec")
            compile((tree / "winbuild/build_prepare.py").read_text(), "build_prepare.py", "exec")
    bundle_root = root / "bundle-check"
    (bundle_root / "size_experiment").mkdir(parents=True)
    script = bundle_root / "size_experiment/deps.py"
    shutil.copyfile(repo / "scripts/deps.py", script)
    prefix = bundle_root / "prefix"
    (prefix / "lib").mkdir(parents=True)
    sample = prefix / "lib/test-library.a"
    sample.write_bytes(b"original-library")
    subprocess.run([sys.executable, str(script), "save", str(prefix)], check=True)
    sample.write_bytes(b"modified")
    subprocess.run([sys.executable, str(script), "restore", str(prefix)], check=True)
    assert sample.read_bytes() == b"original-library"
    result = subprocess.run([sys.executable, str(script), "restore", str(bundle_root / "wrong-prefix")], capture_output=True)
    assert result.returncode != 0 and b"AssertionError" in result.stderr
    archive = bundle_root / "dependency-bundle/deps.tar"
    with archive.open("ab") as stream:
        stream.write(b"corruption")
    result = subprocess.run([sys.executable, str(script), "restore", str(prefix)], capture_output=True)
    assert result.returncode != 0 and b"checksum mismatch" in result.stderr
print("All stage partitioning, Python syntax, archive round-trip, prefix and checksum checks passed")
