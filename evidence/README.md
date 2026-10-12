# Archived evidence

Final experiment: 30 logical platform/configuration pairs, all successful build
and selected test jobs. Five platforms × (`no-jxl`, `pr`, `decoder`, `minsize`,
`lto`, `scalar`). [summary.json](summary.json) records exact byte counts, added
cost, pytest counts, and links to the successful build/test job for each pair.
The [final analysis](../ANALYSIS.md) explains the conclusions and limits.

## Build and test sources

| Platform/configuration | Artifact source |
| --- | --- |
| macOS arm64, all six | [38304925834](https://github.com/EwoutH/jpeg-xl-wheel-size/actions/runs/38304925834) |
| Windows AMD64, all six | [38306989036](https://github.com/EwoutH/jpeg-xl-wheel-size/actions/runs/38306989036) |
| Linux aarch64, all six; Linux x86_64 except PR | [38308512861](https://github.com/EwoutH/jpeg-xl-wheel-size/actions/runs/38308512861) |
| Linux x86_64, PR | [38309406995](https://github.com/EwoutH/jpeg-xl-wheel-size/actions/runs/38309406995) |
| macOS x86_64, all six | [38306998901](https://github.com/EwoutH/jpeg-xl-wheel-size/actions/runs/38306998901) |

Some source runs have an overall failure because another platform/configuration
failed before a focused retry. Only successful build and test jobs contribute
to the final matrix. The evidence validation checks their job conclusions as
well as the measurement and JUnit files. Historical duplicate Windows baseline
artifacts are kept; latest-source platform/configuration pairs are used once in
the final totals. Historical failed variants' patches may also be present; they
do not contribute wheel measurements or test results to the final matrix.

`raw/run-*/` preserves the downloaded artifacts' small files: `sizes.json` (wheel
SHA-256 and member sizes), `verification.json` (availability, sample hashes and
independent-runner timings), `tests.xml` (JUnit), `variant.patch` where present,
and `run.json` (run SHA, job status/steps, times and URLs). These are public CI
metadata, not native build directories. Applied patches are harness patches;
their referenced helper scripts are available at each run's repository SHA.

## Same-host decoding comparisons

| Platform | Source run | Local archive |
| --- | --- | --- |
| Linux x86_64 | [38311876833](https://github.com/EwoutH/jpeg-xl-wheel-size/actions/runs/38311876833) | [controlled/linux-x86_64](controlled/linux-x86_64) |
| Linux aarch64 | [38311817664](https://github.com/EwoutH/jpeg-xl-wheel-size/actions/runs/38311817664) | [controlled/linux-aarch64](controlled/linux-aarch64) |
| macOS x86_64 | [38311818637](https://github.com/EwoutH/jpeg-xl-wheel-size/actions/runs/38311818637) | [controlled/macos-x86_64](controlled/macos-x86_64) |
| macOS arm64 | [38308643532](https://github.com/EwoutH/jpeg-xl-wheel-size/actions/runs/38308643532) | [controlled/macos-arm64](controlled/macos-arm64) |
| Windows AMD64 | [38308639837](https://github.com/EwoutH/jpeg-xl-wheel-size/actions/runs/38308639837) | [controlled/windows-amd64](controlled/windows-amd64) |

Each archive contains per-image medians/hashes, quantified channel differences,
host records, the CI report and run/job provenance. `controlled` is the archive
directory name; these are sequential same-host microbenchmarks, with the load,
thermal and fixed-order limitations described in the analysis.

## Reports and retention

[38312289539](https://github.com/EwoutH/jpeg-xl-wheel-size/actions/runs/38312289539)
combined all source runs without compilation and repacked the saved wheels at
ZIP level 9, verifying identical member bytes. [reports](reports) preserves its
unmodified output, including the PyPI JSON snapshot with version and fetch time.
The root [RESULTS.md](../RESULTS.md) and
[UPSTREAM-COMPARISON.md](../UPSTREAM-COMPARISON.md) contain those final tables.

The native wheels remain downloadable from the source CI runs for the configured
30-day retention period; dependency bundles have 14-day retention. Those large
binaries are not committed. This metadata archive and the charts are committed
so the evidence survives artifact expiry. Wheel SHA-256 values identify exactly
which binaries were measured.

The figure and final narratives can be regenerated offline from the committed
evidence (Matplotlib is needed for the figure):

```console
python scripts/write_final_analysis.py
python scripts/plot_overhead.py
python scripts/analyze.py evidence/raw --output metadata-report.md
```

The last command regenerates metadata tables; reproducing ZIP recompression
requires downloading the actual wheels. To repeat the upstream comparisons,
check out the pinned Pillow source and install its size tool's dependencies,
then use `scripts/compare_upstream.py` with the preserved PyPI snapshot. The
staged build and saved-wheel comparison workflows remain available for a future
expanded matrix; all runs needed for this experiment have finished.
