I finished a **30-wheel experiment across Linux, macOS and Windows**, using this PR's pinned source and a same-commit `no-jxl` baseline. **Linking the existing decoder-only library removes 66–68% of the added Linux/macOS download cost. Adding MinSizeRel and LTO removes about 80–82%, with platform-specific tradeoffs.**

### Added size over `no-jxl`

The reference on each platform is the same Pillow source and base dependencies with JPEG XL disabled. Percentages are **growth over that wheel**, not changes relative to another Pillow release.

![JPEG XL download overhead above no-jxl across five platforms: decoder-only removes 66–68% of the added Linux/macOS cost; MinSizeRel plus LTO removes 80–82%. Windows benefits less.](https://raw.githubusercontent.com/EwoutH/jpeg-xl-wheel-size/master/figures/jpeg-xl-overhead.png)

| Platform | `no-jxl` wheel | PR: full libjxl | Decoder only | + MinSizeRel | + LTO |
| --- | ---: | ---: | ---: | ---: | ---: |
| Linux x86_64 | 6.971 MiB | +29.8% | +10.1% | +6.6% | +5.5% |
| Linux aarch64 | 6.409 MiB | +24.8% | +8.2% | +5.7% | +4.8% |
| macOS x86_64 | 5.283 MiB | +40.9% | +13.0% | +9.0% | +7.5% |
| macOS arm64 | 4.565 MiB | +29.1% | +9.4% | +7.0% | +5.9% |
| Windows AMD64 | 6.793 MiB | +8.5% | +8.5% | +6.9% | +6.9% |

For example, Intel macOS falls from **+2.161 MiB** with the PR to **+0.397 MiB** with decoder-only + MinSizeRel + LTO. Linux x86_64 falls from **+2.080 MiB to +0.386 MiB**. These are reductions in the *added codec cost*, not 80% reductions in the whole Pillow wheel.

Installed payload shrinks too: on Intel macOS, the extra uncompressed contents fall from **6.032 to 1.173 MiB**; on Linux x86_64, **5.274 to 1.024 MiB**.

<details>
<summary>Absolute wheel download sizes (MiB)</summary>

| Platform | `no-jxl` | PR | Decoder only | + MinSizeRel | + LTO |
| --- | ---: | ---: | ---: | ---: | ---: |
| Linux x86_64 | 6.971 | 9.052 | 7.676 | 7.435 | 7.357 |
| Linux aarch64 | 6.409 | 7.998 | 6.934 | 6.771 | 6.717 |
| macOS x86_64 | 5.283 | 7.443 | 5.970 | 5.759 | 5.680 |
| macOS arm64 | 4.565 | 5.894 | 4.993 | 4.885 | 4.835 |
| Windows AMD64 | 6.793 | 7.368 | 7.368 | 7.262 | 7.262 |

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
