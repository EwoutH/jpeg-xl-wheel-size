I’ve been testing ways to reduce the wheel-size impact of this PR. Initial results suggest that linking libjxl’s existing decoder-only target is a useful first step, with additional savings possible from size optimization and LTO.

The [experiment repository](https://github.com/EwoutH/jpeg-xl-wheel-size) builds real CPython 3.13 wheels from this PR’s pinned commit, `d00ba3a89faabd31fd92c3b506c86557da8c0a0b`, using libjxl 0.11.2 and Pillow’s dependency recipes. Each platform has a baseline from the same source with JPEG XL disabled, so these comparisons isolate the added codec cost.

Wheel download sizes, in **MiB**:

| Platform | JPEG XL disabled | PR settings | Decoder only | + MinSizeRel | + LTO |
| --- | ---: | ---: | ---: | ---: | ---: |
| Linux aarch64 | 6.409 | 7.998 | 6.934 | 6.771 | 6.717 |
| macOS arm64 | 4.565 | 5.894 | 4.993 | 4.885 | 4.835 |
| Windows AMD64 | 6.793 | 7.368 | 7.368 | 7.262 | 7.262 |

Decoder-only linking reduces the total wheel by **13.3% on Linux aarch64** and **15.3% on macOS arm64**, removing approximately two-thirds of the JPEG XL overhead. With MinSizeRel and LTO, the added download cost falls from about **1.589 to 0.307 MiB** on Linux aarch64 and **1.330 to 0.270 MiB** on macOS arm64—roughly **80% less JPEG XL overhead**. These builds also reduce uncompressed wheel size: from 25.317 to 21.872 MiB on Linux aarch64 and from 14.804 to 12.182 MiB on macOS arm64.

The smaller Windows improvement is consistent with its existing static linking, where unused encoder objects can already be discarded. Size optimization saves about 1.4% of the total Windows wheel; LTO adds little download-size benefit there.

The decoder variant links `jxl_dec` and `jxl_threads`, adds an install rule for the upstream decoder target on Unix, and omits the encoder-only Brotli link on Windows. It retains box/metadata decoding, animation and JPEG reconstruction support. Standalone tools and benchmarks are excluded from the optimized builds. The Linux x86_64 PR baseline also needs those executables disabled because a benchmark fails to link against the common static libsharpyuv archive; its codec library and optimization settings remain unchanged.

All variants in the table passed Pillow’s selftest and the selected JPEG XL, JPEG and PNG tests: **195 passed / 1 skipped** on macOS arm64 and **194 passed / 2 skipped** on Linux aarch64 and Windows. Same-runner comparisons of six sample images found identical decoded pixels for decoder-only, MinSizeRel and LTO on macOS arm64 and Windows. Linux aarch64’s sample hashes also matched across its independent test jobs.

There are performance tradeoffs. In the same-runner sample measurements, macOS arm64 LTO decoding was close to the PR, while Windows MinSizeRel/LTO took roughly 1.4–1.5× as long for the two flower samples. These are initial microbenchmarks, not controlled release-wide performance results. Decoder-only linking looks like the clearest first change; compiler optimization choices deserve broader benchmarking.

I also tested scalar-only Highway compilation. It saved relatively little beyond LTO, changed some decoded channel values by one level, and was substantially slower. I would not propose that as the default. Repacking the wheels at ZIP level 9 saved only around 0.1–0.2%, without reducing installed size.

The reporting now reuses Pillow’s wheel-tag matching and table rendering from **#9621**, alongside per-member sizes and decoding checks. The same-commit baseline is used for the JPEG XL conclusions; the PyPI comparison also includes unrelated changes. Builds use staged, cached dependency bundles, and wheels are uploaded before testing, so analysis and test retries do not require another native build.

These are preliminary results: the optimized Linux x86_64 wheels have passed, but its PR baseline retry and the Intel macOS builds are still running. This covers one Python ABI and a small image corpus, rather than Pillow’s complete release matrix or full codec qualification.

References: [size/test report](https://github.com/EwoutH/jpeg-xl-wheel-size/actions/runs/38309369474), [same-runner macOS comparison](https://github.com/EwoutH/jpeg-xl-wheel-size/actions/runs/38308643532), [same-runner Windows comparison](https://github.com/EwoutH/jpeg-xl-wheel-size/actions/runs/38308639837), [build scripts and methodology](https://github.com/EwoutH/jpeg-xl-wheel-size).
