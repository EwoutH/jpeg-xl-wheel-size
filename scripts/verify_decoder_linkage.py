"""Verify that repaired Unix wheels carry the decoder library, not the encoder."""
import re
import sys
from pathlib import Path
from zipfile import ZipFile

for path in Path("wheelhouse").glob("*.whl"):
    with ZipFile(path) as wheel:
        names = wheel.namelist()
    if sys.platform == "win32":
        assert any("_jpegxl" in name and name.endswith(".pyd") for name in names)
    else:
        assert any("libjxl_dec" in name for name in names), names
        assert any("libjxl_threads" in name for name in names), names
        assert not any(re.search(r"/libjxl[.-]", name) for name in names), names
        assert not any("libjxl_cms" in name for name in names), names
    print(f"Verified decoder-only native payload: {path}")
