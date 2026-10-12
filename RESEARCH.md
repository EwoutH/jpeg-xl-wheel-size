# JPEG XL wheel-size research

## Question and controls

Can Pillow include the read-only JPEG XL implementation in PR #7848 with a
materially smaller binary cost? The PR discussion reports a substantial wheel
increase, particularly on Unix. Those historical percentages are motivation,
not measurements from this experiment.

The measurements here use one pinned source commit, one Python ABI, and the
same base dependency recipes. `no-jxl` disables only the JPEG XL extension; it
does not substitute a different Pillow release. Compare each platform against
its own baseline. Do not sum five representative wheels and extrapolate that
percentage to Pillow's whole release matrix.

## Options under test

1. **Use the existing decoder-only library.** In libjxl 0.11.2, `jxl` combines
   encoder and decoder objects; `jxl_dec` contains decoder objects and omits the
   encoder's Brotli dependency. Pillow's PR calls decoder and threading APIs.
   The Unix recipes install the full shared library, so encoder API exports can
   retain code that Pillow never calls. Windows already uses static archives
   and can discard unreferenced objects, so a smaller improvement is expected
   there. This is a hypothesis until wheels and tests complete.
2. **Optimize libjxl for size.** Compare `MinSizeRel` against the decoder-only
   build. This changes libjxl compilation, rather than degrading other Pillow
   codecs. Compilers may trade decoding speed for smaller code.
3. **Enable LTO.** CMake interprocedural optimization can eliminate more unused
   code and fold functions. The experiment enables it for libjxl; separately
   built Highway and Brotli retain their existing Pillow recipes. This is not
   a claim of whole-program optimization across every bundled dependency.
4. **Restrict Highway to scalar code.** This measures the size of architecture
   specialization and dispatch. It is deliberately an aggressive tradeoff,
   and is not a recommendation unless performance and compatibility justify it.
5. **Recompress wheel ZIPs at level 9.** This only reduces transfer/storage
   bytes. The script writes actual repacked wheels and verifies every member
   against the original, including RECORD. It does not reduce installed size.

The decoder-only target is an upstream target but is not normally installed.
The experiment adds an install rule and changes Pillow's detection/linking to
use `jxl_dec` with `jxl_threads`. It does not replace `libjxl` with a partial
library under the full library's name. The original full library may remain in
the build prefix; wheel repair should bundle only actual runtime dependencies.
The per-member measurements make that check reviewable.

Box decoding, compressed metadata, animations, bit depths and JPEG
reconstruction are retained. Disabling these features could reduce size, but
would narrow image support and needs an explicit product decision.

## Architectural alternatives

**An optional plugin/extra** keeps the core Pillow wheel unchanged and gives
users who need JPEG XL a separate download. The Pillow maintainers' issue #9101
discusses maintaining selected plugins under the python-pillow organization
and exposing them as extras. An extra can install another distribution, but
does not automatically register its image plugin; registration/import behavior
needs to be designed and tested. No packaging redesign is claimed as a tested
result here. Codec size optimization remains useful for the optional wheel.

**Shared codec distributions** can avoid shipping the same native decoder in
every Python ABI wheel, at the cost of native dependency loading, versioning,
repair tooling and platform support. **Stable-ABI extension wheels** could also
reduce the number of release artifacts, but require a separate C API audit;
they do not directly reduce an individual user's installed decoder size.

**External system libraries** are reasonable for source/conda/distribution
builds but are not a substitute for self-contained pip wheels. Simply removing
a required shared library from a wheel would produce a broken installation.

## Validation and limits

CI runs Pillow's selftest first, asserts the intended JPEG XL availability, then
runs the PR's JPEG XL image, animation and metadata tests plus JPEG/PNG regression
tests. The artifact records decoded sample hashes and median warm decoding
times. Test skips for optional dependencies must be read alongside pass counts.
The experiment does not claim full Pillow release qualification, fuzzing,
cross-architecture equivalence, or a controlled performance benchmark.

The initial platform matrix covers Linux glibc x86_64/aarch64, macOS
x86_64/arm64, and Windows AMD64. musllinux, Windows ARM64/x86, PyPy,
free-threaded Python and older CPython versions need follow-up before an
upstream release decision.

## Primary sources

- [Pillow JPEG XL PR](https://github.com/python-pillow/Pillow/pull/7848)
- [Pillow plugin packaging discussion](https://github.com/python-pillow/Pillow/issues/9101)
- [libjxl 0.11.2 library targets](https://github.com/libjxl/libjxl/blob/v0.11.2/lib/jxl.cmake)
- [libjxl build options](https://github.com/libjxl/libjxl/blob/v0.11.2/CMakeLists.txt)
- [Highway target selection](https://github.com/google/highway/blob/1.3.0/hwy/detect_targets.h)
- [CMake interprocedural optimization setting](https://cmake.org/cmake/help/latest/variable/CMAKE_INTERPROCEDURAL_OPTIMIZATION.html)
