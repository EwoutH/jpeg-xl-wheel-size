"""Install libjxl's existing decoder target without changing its implementation."""
from __future__ import annotations

import sys
from pathlib import Path

root = Path(sys.argv[1])
path = root / "lib/jxl.cmake"
text = path.read_text()
assert "add_library(jxl_dec $<TARGET_OBJECTS:jxl_dec-obj>)" in text
assert "install(TARGETS jxl_dec" not in text
text += """
# Wheel-size experiment: bundle the upstream decoder-only target.
install(TARGETS jxl_dec
  RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
  LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
  ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR})
"""
path.write_text(text)
