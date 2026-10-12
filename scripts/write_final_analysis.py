"""Generate final analysis and the postable comment from archived measurements."""
from pathlib import Path
import json

repo = Path(__file__).resolve().parents[1]
summary = json.loads((repo / "evidence/summary.json").read_text())
rows = summary["platforms"]
names = {"linux-x86_64": "Linux x86_64", "linux-aarch64": "Linux aarch64",
         "macos-x86_64": "macOS x86_64", "macos-arm64": "macOS arm64", "windows-amd64": "Windows AMD64"}
variants = ("pr", "decoder", "minsize", "lto")

def table(header, values):
    return "\n".join(["| " + " | ".join(header) + " |", "| --- | " + " | ".join(["---:"] * (len(header)-1)) + " |"] + ["| " + " | ".join(row) + " |" for row in values])

growth = table(["Platform", "`no-jxl` wheel", "PR: full libjxl", "Decoder only", "+ MinSizeRel", "+ LTO"],
               [[names[p], f'{r["no-jxl"]["bytes"]/1048576:.3f} MiB'] + [f'{r[v]["growth_percent"]:+.1f}%' for v in variants] for p, r in rows.items()])
absolute = table(["Platform", "`no-jxl`", "PR", "Decoder only", "+ MinSizeRel", "+ LTO"],
                 [[names[p]] + [f'{r[v]["bytes"]/1048576:.3f}' for v in ("no-jxl", *variants)] for p, r in rows.items()])
added = table(["Platform", "PR added MiB", "Decoder added MiB", "LTO added MiB", "Added cost removed by LTO", "Whole wheel smaller vs PR"],
              [[names[p]] + [f'{r[v]["added_bytes"]/1048576:.3f}' for v in ("pr", "decoder", "lto")] + [f'{r["lto"]["overhead_removed_percent"]:.1f}%', f'{100*(1-r["lto"]["bytes"]/r["pr"]["bytes"]):.1f}%'] for p, r in rows.items()])
installed = table(["Platform", "`no-jxl` MiB", "PR added MiB", "Decoder added MiB", "LTO added MiB"],
                  [[names[p], f'{r["no-jxl"]["installed_bytes"]/1048576:.3f}'] + [f'{r[v]["added_installed_bytes"]/1048576:.3f}' for v in ("pr", "decoder", "lto")] for p, r in rows.items()])
timings = []
pixels = []
for p in names:
    folder = repo / "evidence/controlled" / p
    baseline = sum(x["seconds"] for x in json.loads((folder / "pr/samples.json").read_text()))
    timings.append([names[p]] + [f'{sum(x["seconds"] for x in json.loads((folder / v / "samples.json").read_text()))/baseline:.2f}×' for v in ("decoder", "minsize", "lto", "scalar")])
    comparisons = json.loads((folder / "comparison.json").read_text())["comparisons"]
    pixels.append([names[p]] + [str(sum(x["changed"] for x in comparisons if x["variant"] == v)) for v in ("decoder", "minsize", "lto", "scalar")])
performance = table(["Platform", "Decoder only", "+ MinSizeRel", "+ LTO", "Scalar only"], timings)
pixel_table = table(["Platform", "Decoder only", "+ MinSizeRel", "+ LTO", "Scalar only"], pixels)
figure = "![JPEG XL download overhead above no-jxl across five platforms: decoder-only removes 66–68% of the added Linux/macOS cost; MinSizeRel plus LTO removes 80–82%. Windows benefits less.](https://raw.githubusercontent.com/EwoutH/jpeg-xl-wheel-size/master/figures/jpeg-xl-overhead.png)"

comment = f"""I finished a **30-wheel experiment across Linux, macOS and Windows**, using this PR's pinned source and a same-commit `no-jxl` baseline. **Linking the existing decoder-only library removes 66–68% of the added Linux/macOS download cost. Adding MinSizeRel and LTO removes about 80–82%, with platform-specific tradeoffs.**

### Added size over `no-jxl`

The reference on each platform is the same Pillow source and base dependencies with JPEG XL disabled. Percentages are **growth over that wheel**, not changes relative to another Pillow release.

{figure}

{growth}

For example, Intel macOS falls from **+2.161 MiB** with the PR to **+0.397 MiB** with decoder-only + MinSizeRel + LTO. Linux x86_64 falls from **+2.080 MiB to +0.386 MiB**. These are reductions in the *added codec cost*, not 80% reductions in the whole Pillow wheel.

Installed payload shrinks too: on Intel macOS, the extra uncompressed contents fall from **6.032 to 1.173 MiB**; on Linux x86_64, **5.274 to 1.024 MiB**.

<details>
<summary>Absolute wheel download sizes (MiB)</summary>

{absolute}

MiB = 1,048,576 bytes. Values are rounded independently.

</details>

### What looks worth pursuing

1. **Decoder-only linking is the clearest first change.** The experiment installs and links upstream `jxl_dec` with `jxl_threads`, and omits the encoder-only Brotli link on Windows. It retains box/metadata decoding, animation and JPEG reconstruction. Decoder-only sample pixels matched the PR exactly on all five platforms when compared on the same host. Windows' existing static linking already eliminates much unused encoder code, so it gains essentially no download-size reduction from this change alone.
2. **Evaluate MinSizeRel/LTO by platform.** They bring Linux/macOS growth down to **4.8–7.5%** above `no-jxl`, but are not a universally free optimization. On Windows, LTO saved about **1.4% of the whole wheel** and took **1.4–1.5× as long** on two flower samples. On Linux x86_64, MinSizeRel and LTO each changed six of 914,628 sample channel values by one level; the other four platforms matched exactly for these variants. Investigate those rounding differences and benchmark a broader corpus before choosing release flags.
3. **ZIP level 9 is a useful separate Linux option.** Repacking saved **3.0–3.7%** of Linux wheel bytes, versus **0.14–0.33%** on macOS/Windows. Every unpacked member, including RECORD, remained byte-for-byte identical; installed size is unchanged. The table above uses original, unrepacked wheels consistently.
4. **Keep SIMD enabled.** Scalar-only builds saved another **12–126 KiB** beyond LTO, but changed more sample pixels and took approximately **2–4× as long** for the flower samples. I would not propose this as the default.

### Validation and reproducibility

All **30 builds and selected test jobs passed**: Pillow selftest, JPEG XL availability assertions, and the PR's JPEG XL tests plus JPEG/PNG regressions. Across the 30 deduplicated pytest results there were **5,742 passed, 138 skipped, and zero failures/errors**. The skips include deliberately disabled JPEG XL in baseline wheels. Five separate jobs compared saved wheels on the same host, avoiding cross-runner CPU differences; timings remain exploratory because host load, thermals and fixed benchmark order are not controlled.

The [repository](https://github.com/EwoutH/jpeg-xl-wheel-size) contains the [final analysis](https://github.com/EwoutH/jpeg-xl-wheel-size/blob/master/ANALYSIS.md), [raw evidence, checksums and applied patches](https://github.com/EwoutH/jpeg-xl-wheel-size/tree/master/evidence), and [combined CI report](https://github.com/EwoutH/jpeg-xl-wheel-size/actions/runs/38312289539). Source: `d00ba3a89faabd31fd92c3b506c86557da8c0a0b`, CPython 3.13, libjxl 0.11.2. Reporting reuses Pillow's #9621 matching/table functions. The five representative platform tags are not the complete Pillow release matrix, and six sample images are not full codec qualification.

Standalone tools/benchmarks are excluded from optimized builds. The Linux x86_64 PR baseline also needed them disabled to avoid a standalone benchmark's libsharpyuv link failure; its codec library and optimization settings remain unchanged. Builds use cached common dependency bundles, with wheels saved before tests, so reporting and test retries do not recompile libraries.
"""
(repo / "PR7848-COMMENT.md").write_text(comment, encoding="utf-8")

analysis = f"""# Final analysis: Pillow JPEG XL wheel size

Completed on 12 October 2026: **30 wheels, five platforms, six configurations, 30 successful selected test jobs**, and five same-host decoding comparisons. The most defensible first change is linking libjxl's existing decoder-only target. That removes 66–68% of the JPEG XL download overhead on Linux/macOS without changing decoded pixels in the six samples tested on any platform. Size optimization and LTO remove about 80–82%, but introduce measurable performance and rounding tradeoffs. Windows has much less to gain because the existing recipe links static libraries.

## Controls and configurations

Pillow is pinned to `olokelo/Pillow@d00ba3a89faabd31fd92c3b506c86557da8c0a0b`, the PR #7848 head used for this experiment. It builds CPython 3.13 wheels with libjxl 0.11.2, Highway 1.3.0 and Pillow's own dependency recipes. The platforms are Linux glibc x86_64/aarch64, macOS x86_64/arm64, and Windows AMD64.

Each platform builds its common dependencies once and restores that installed prefix for fresh variant builds. Its `no-jxl` wheel explicitly disables the extension in the same source; it is not a different Pillow release. Linux variants use the common stage's pinned manylinux container digest. Runner/toolchain cache keys and immutable, checksummed dependency artifacts prevent mixing prefixes across variants.

| Configuration | Change |
| --- | --- |
| `no-jxl` | Same source, JPEG XL explicitly disabled |
| `pr` | PR codec library/compiler settings |
| `decoder` | Link/install upstream `jxl_dec`; retain `jxl_threads`; omit encoder-only Windows Brotli link |
| `minsize` | Decoder build plus `CMAKE_BUILD_TYPE=MinSizeRel` |
| `lto` | Previous configuration plus `CMAKE_INTERPROCEDURAL_OPTIMIZATION=ON` |
| `scalar` | Previous configuration plus `HWY_COMPILE_ONLY_SCALAR` in libjxl C/C++ compilation |

The decoder variants retain SIMD, box decoding, compressed metadata, animations, bit depths and JPEG reconstruction; scalar alone changes SIMD policy. No format features were deliberately removed. LTO applies to libjxl, not every separately built Pillow dependency.

## Download size against the no-jxl reference

{figure}

{growth}

{added}

The Unix decoder-only result is consistent across architectures: it removes about two-thirds of the added codec cost. MinSizeRel/LTO shrink the remaining code further. The 80–82% figure describes the *added JPEG XL overhead*, not the whole wheel. The total Unix wheels become 16.0–23.7% smaller than the corresponding PR wheels.

On Windows, decoder-only linking has effectively no size benefit; the main native extension is exactly 1,482,240 bytes uncompressed in both PR and decoder-only wheels. The static linker already removes much unreferenced code. MinSizeRel supplies almost all the Windows download-size improvement; LTO makes little further difference to ZIP bytes.

Absolute original wheel sizes (MiB):

{absolute}

## Installed payload and where the savings come from

Uncompressed member bytes approximate installed payload, excluding generated bytecode, filesystem block allocation and installer-generated files. The columns below are additions over each platform's uncompressed `no-jxl` wheel.

{installed}

Per-member evidence confirms that optimized Unix wheels bundle `libjxl_dec` instead of the full `libjxl`; the separately bundled `libjxl_cms` dependency is also absent. On Linux x86_64 the main codec library shrinks from 4,545,441 bytes (`libjxl`) to 1,831,585 (`jxl_dec`) and 979,969 (size-optimized/LTO `jxl_dec`). On Intel macOS, the same progression is 5,330,208 → 2,140,416 → 1,152,864 bytes. Threading and Pillow's small codec extension remain present. Windows embeds the decoder in `_jpegxl.pyd`, which shrinks to 1,174,528 bytes with LTO.

These member sizes explain the mechanism more directly than comparing total ZIP sizes alone. They also show that the optimized wheel is not still carrying the original full shared decoder/encoder library under another filename.

## Pixel equivalence and decoding speed

Five jobs installed each saved wheel into a separate directory and ran all configurations sequentially on the same host, in separate Python processes. Six JPEG XL samples cover RGB, grayscale, transparency and 16-bit data. Pixel comparisons used decoded arrays, with maximum absolute channel differences and counts of changed channel values. This is more informative than comparing hashes from different hosted CPUs.

Changed channel values against the PR, out of **914,628 across the six samples**:

{pixel_table}

All nonzero differences in this corpus are at most **one channel level**, in 8-bit samples; the tested transparent and 16-bit sample outputs match. Decoder-only matches exactly on all platforms. Linux x86_64's size-optimized variants each differ in six channel values across three images, and these differences persist on the same host. Do not claim universal pixel identity for those flags. The scalar variant changes more values on all five platforms. Passing the existing tests does not resolve every rounding or conformance question; a larger corpus is needed before accepting a numerical change.

Relative decoding time, computed as the sum of the six sample median times divided by the corresponding sum for PR (lower is faster):

{performance}

Each sample uses eleven batches of ten decodes, taking a median. The same-host setup removes cross-runner CPU variation but does not control shared-host load, thermals, CPU frequency or order: PR always runs first. Apparent macOS speedups should therefore not be treated as established performance improvements. On Windows the two flower samples take about 1.4–1.5× as long with MinSizeRel/LTO, while Linux aarch64 LTO takes about 1.16× for those samples. Scalar takes approximately 2–4× as long for the flower samples across these hosts. Detailed per-image timings and host records are committed under [evidence/controlled](evidence/controlled).

Initial independent-runner Windows hash differences disappeared in the same-host comparison. Linux x86_64's six size-optimization differences did not. The [raw per-runner report](RESULTS.md) is preserved for audit, but this same-host analysis takes precedence for interpretation.

## ZIP compression and other packaging options

Repacking the actual wheels with DEFLATE level 9 saves **2.97–3.65% on Linux** and **0.14–0.33% on macOS/Windows**. The optimized Linux LTO wheels save about 229–249 KiB. All ZIP members were verified byte-for-byte identical, including RECORD, so installed payload and native code do not change. This is a worthwhile separate Linux packaging option. It is not a JPEG XL-specific saving: the no-jxl wheels also shrink. All size tables above consistently use the original wheels; [RESULTS.md](RESULTS.md) records the separate recompression measurements.

Scalar-only compilation saves another 12–126 KiB beyond LTO, at the substantial numerical/performance cost shown above. It is not recommended as the default.

An optional plugin/extra, as discussed in Pillow #9101, could keep JPEG XL's native cost out of the core wheel entirely. That requires a separate distribution, plugin registration/loading design and packaging tests; it was researched but not built here. Shared codec distributions and stable-ABI extensions could reduce repeated release payload across Python versions, but require native loading/versioning or a C API audit. External system libraries are a source/distribution packaging option, not an equivalent self-contained pip wheel. None of these architectural alternatives is claimed as a measured result.

## Test evidence, provenance and limitations

All 30 selected test jobs passed Pillow selftest and the intended JPEG XL availability assertion, followed by the PR's JPEG XL image/animation/metadata tests and JPEG/PNG regression tests. Deduplicated pytest totals are **5,742 passed, 138 skipped, zero failures and zero errors** across 5,880 test cases. Each job collects 196 tests; the skips include the intentionally disabled JPEG XL baseline and platform/optional-feature skips. The 25 codec-enabled wheels pass their targeted codec tests; baseline absence is explicitly asserted.

The [evidence index](evidence/README.md) links every source run and documents the archive. Committed data include all 30 wheel measurements with full member sizes and wheel SHA-256, verification results, JUnit XML, applied variant patches, run/job metadata, five same-host comparisons, and the PyPI snapshot. Duplicate baseline artifacts are retained for provenance but deduplicated by platform/configuration in the final totals.

Pillow #9621's unmodified matching and table-rendering functions produce [UPSTREAM-COMPARISON.md](UPSTREAM-COMPARISON.md). Its PyPI baseline is recorded in [the snapshot](evidence/reports/pypi-baseline.json), including release version and fetch time. PyPI comparisons include unrelated changes and possibly different platform tags. The causal JPEG XL conclusions use the same-commit no-jxl reference. Totals over five representative platform tags do not represent Pillow's complete release matrix.

The harness skips Highway standalone tests/examples. Optimized builds disable standalone libjxl tools, examples, benchmarks and documentation. For the final Linux x86_64 PR baseline, standalone tools/benchmarks were disabled after a benchmark failed to link against the common non-PIE libsharpyuv archive. Library/compiler settings remain the PR's; those executables are not wheel payload. Applied patches show the actual settings used by each historical run. The research harness is not a ready-to-merge upstream patch: its decoder install helper must be integrated into Pillow's production dependency recipe.

This is not full Pillow release qualification or fuzzing. It covers one CPython ABI, the tested hosted OS versions, glibc Linux and six benchmark images. musllinux, Windows ARM64/x86, PyPy, free-threaded builds, other CPython versions and minimum supported operating systems need separate validation. A broader image corpus and repeated, randomized benchmark order would be needed for release-wide speed or pixel-equivalence claims.

## Build cost and recommended next steps

The staged pipeline compiles common dependencies once per platform, then fans out the five JPEG XL builds; `no-jxl` reuses the saved baseline wheel. Common installed prefixes are cached with exact toolchain/recipe keys and saved as checksummed artifacts. Wheels and measurements upload before separate tests. Focused retries can restore a previous common bundle, and reports/same-host comparisons use saved wheels with no compilation. The original imposed ten-job cap was removed; account/runner capacity still limits concurrency.

The archived Windows common job fell from **634 seconds to 31 seconds** when restoring its bundle. Linux common-stage reuse took **46–49 seconds** in the final retries. This is measured reuse of those jobs, not a claim that every CI stage became twenty times faster. It also avoids rebuilding unrelated codecs for each libjxl configuration. Wheel/test artifacts remain subject to their CI retention periods; the small evidence archive is committed so the analysis survives artifact expiry.

1. Integrate upstream `jxl_dec` detection, installation and linking into the Pillow PR; retain threading and format features. This has the strongest size/compatibility result in this experiment.
2. Consider size flags/LTO separately by platform. Investigate Linux x86_64 rounding differences and broaden performance tests, especially before accepting Windows' small size gain with slower decoding.
3. Evaluate ZIP level 9 in the Linux packaging stage independently of the codec changes. It reduces download bytes while preserving member contents.
4. Keep SIMD in the default build. Treat optional plugin packaging as a separate architectural decision, informed by the now-smaller codec cost.

Sources: [Pillow PR #7848](https://github.com/python-pillow/Pillow/pull/7848), [plugin discussion #9101](https://github.com/python-pillow/Pillow/issues/9101), [Pillow size tool #9621](https://github.com/python-pillow/Pillow/pull/9621), [libjxl 0.11.2 library targets](https://github.com/libjxl/libjxl/blob/v0.11.2/lib/jxl.cmake), [Highway 1.3.0 target selection](https://github.com/google/highway/blob/1.3.0/hwy/detect_targets.h), and the linked CI evidence.
"""
(repo / "ANALYSIS.md").write_text(analysis, encoding="utf-8")
print("Wrote ANALYSIS.md and PR7848-COMMENT.md from the archived final measurements")
