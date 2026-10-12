"""Test an already-uploaded wheel; a failure never discards its build artifact."""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1] / "Pillow"
os.chdir(root)
subprocess.run([sys.executable, "selftest.py"], check=True)
subprocess.run([sys.executable, "size_experiment/verify.py"], check=True)
subprocess.run([sys.executable, "-m", "pytest", "-v", "-ra", "--junitxml=size_experiment/tests.xml",
                "Tests/test_file_jxl.py", "Tests/test_file_jxl_animated.py", "Tests/test_file_jxl_metadata.py",
                "Tests/test_file_jpeg.py", "Tests/test_file_png.py"], check=True)
