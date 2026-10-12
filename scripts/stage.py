"""Split upstream dependency recipes into common and JPEG XL-only stages."""
from __future__ import annotations

import argparse
import shutil
from pathlib import Path

from prepare import replace

parser = argparse.ArgumentParser()
parser.add_argument("root", type=Path)
parser.add_argument("stage", choices=("common", "variant"))
args = parser.parse_args()
root = args.root
shutil.copyfile(Path(__file__).with_name("deps.py"), root / "size_experiment/deps.py")
commands = ['@echo off', 'call winbuild\\build\\build_env.cmd', 'if errorlevel 1 exit /b 1']
if args.stage == "common":
    commands += ['call winbuild\\build\\build_dep_all.cmd', 'if errorlevel 1 exit /b 1',
                 'python size_experiment\\deps.py save winbuild\\build --windows']
else:
    commands += ['python size_experiment\\deps.py restore winbuild\\build --windows', 'if errorlevel 1 exit /b 1',
                 'call winbuild\\build\\build_dep_highway.cmd', 'if errorlevel 1 exit /b 1',
                 'call winbuild\\build\\build_dep_libjxl.cmd', 'if errorlevel 1 exit /b 1']
(root / "size_experiment/windows_deps.cmd").write_text('\n'.join(commands) + '\n')
native = root / ".github/workflows/wheels-dependencies.sh"
win = root / "winbuild/build_prepare.py"
if args.stage == "common":
    replace(native, "        build_jpegxl\n", "        : # JPEG XL is built by the variant stage\n")
    replace(native, "wrap_wheel_builder build\n", 'wrap_wheel_builder build\npython3 "$PROJECTDIR/size_experiment/deps.py" save "$BUILD_PREFIX"\n')
    replace(win, "    disabled = []\n", '    disabled = ["libjxl"]\n')
else:
    text = native.read_text()
    highway_start = text.index('function build_jpegxl {\n')
    highway_end = text.index('    local out_dir=$(fetch_unpack https://github.com/libjxl/', highway_start)
    highway = text[highway_start:highway_end]
    assert highway.count('$HOST_CMAKE_FLAGS .') == 1
    highway = highway.replace('$HOST_CMAKE_FLAGS .', '-DHWY_ENABLE_TESTS=OFF -DHWY_ENABLE_EXAMPLES=OFF -DHWY_ENABLE_CONTRIB=OFF $HOST_CMAKE_FLAGS .')
    text = text[:highway_start] + highway + text[highway_end:]
    start = text.index("function build {\n")
    end = text.index("\nfunction create_meson_cross_config", start)
    text = text[:start] + "function build {\n    build_jpegxl\n}\n" + text[end:]
    start = text.index("if [[ ! -d $WORKDIR/pillow-depends-main ]]; then\n")
    end = text.index('\nif [[ -n "$IS_MACOS" ]]; then', start)
    text = text[:start] + 'python3 "$PROJECTDIR/size_experiment/deps.py" restore "$BUILD_PREFIX"\n' + text[end:]
    text = text.replace("    build_pkg_config\n", "    : # pkg-config is restored from the common bundle\n")
    native.write_text(text, encoding="utf-8", newline="\n")
    # Only download and prepare Highway/libjxl; other installed libraries come
    # from the common bundle. Highway headers are needed by libjxl's recipe.
    replace(win, "    disabled = []\n", '    disabled = [name for name in DEPS if name not in ("highway", "libjxl")]\n')
