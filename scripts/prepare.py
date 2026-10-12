"""Apply narrowly scoped, checked patches to the pinned Pillow experiment tree."""
from __future__ import annotations

import argparse
import shutil
from pathlib import Path

VARIANTS = ("no-jxl", "pr", "decoder", "minsize", "lto", "scalar")


def replace(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    if text.count(old) != 1:
        raise ValueError(f"Expected one match in {path}: {old!r}")
    path.write_text(text.replace(old, new), encoding="utf-8", newline="\n")


def prepare(root: Path, variant: str) -> None:
    dest = root / "size_experiment"
    dest.mkdir(exist_ok=True)
    for name in ("patch_libjxl.py", "verify.py"):
        shutil.copyfile(Path(__file__).with_name(name), dest / name)
    (dest / "variant.txt").write_text(variant, encoding="utf-8")
    if variant in ("pr", "no-jxl"):
        return
    setup = root / "setup.py"
    replace(setup, '_find_library_file(self, "jxl")', '_find_library_file(self, "jxl_dec")')
    replace(setup, 'feature.set("jpegxl", "jxl")', 'feature.set("jpegxl", "jxl_dec")')
    replace(setup, 'libs = [jpegxl, jpegxl + "_threads"]', 'libs = [jpegxl, "jxl_threads"]')
    replace(setup, '["brotlicommon", "brotlidec", "brotlienc", "hwy"]', '["brotlicommon", "brotlidec", "hwy"]')
    native = root / ".github/workflows/wheels-dependencies.sh"
    marker = '    local out_dir=$(fetch_unpack https://github.com/libjxl/libjxl/archive/v$JPEGXL_VERSION.tar.gz)\n'
    replace(native, marker, marker + '    python3 "$PROJECTDIR/size_experiment/patch_libjxl.py" "$out_dir"\n')
    flags = ["-DJPEGXL_ENABLE_TOOLS=OFF", "-DJPEGXL_ENABLE_JPEGLI=OFF",
             "-DJPEGXL_ENABLE_EXAMPLES=OFF", "-DJPEGXL_ENABLE_BENCHMARK=OFF",
             "-DJPEGXL_ENABLE_JNI=OFF", "-DJPEGXL_ENABLE_DOXYGEN=OFF",
             "-DJPEGXL_ENABLE_MANPAGES=OFF"]
    if variant in ("minsize", "lto", "scalar"):
        flags.append("-DCMAKE_BUILD_TYPE=MinSizeRel")
    if variant in ("lto", "scalar"):
        flags.append("-DCMAKE_INTERPROCEDURAL_OPTIMIZATION=ON")
    if variant == "scalar":
        flags += ["-DCMAKE_C_FLAGS=-DHWY_COMPILE_ONLY_SCALAR", "-DCMAKE_CXX_FLAGS=-DHWY_COMPILE_ONLY_SCALAR"]
    replace(native, "-DJPEGXL_ENABLE_SJPEG=OFF -DJPEGXL_ENABLE_SKCMS=OFF -DBUILD_TESTING=OFF",
            "-DJPEGXL_ENABLE_SJPEG=OFF -DJPEGXL_ENABLE_SKCMS=OFF -DBUILD_TESTING=OFF " + " ".join(flags))
    win = root / "winbuild/build_prepare.py"
    replace(win, '                "jxl",\n', '                "jxl_dec",\n' + ''.join(f'                "{flag}",\n' for flag in flags))
    replace(win, 'cmd_copy(r"lib\\jxl.lib", "{lib_dir}")', 'cmd_copy(r"lib\\jxl_dec.lib", "{lib_dir}")')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path)
    parser.add_argument("variant", choices=VARIANTS)
    args = parser.parse_args()
    prepare(args.root, args.variant)
