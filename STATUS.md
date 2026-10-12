# Paused after initial analysis

User requested an initial postable analysis, then a pause. Draft: PR7848-COMMENT.md.
No GitHub issue/PR comment was posted. CI continues independently; no additional
monitoring or builds should be initiated until the user resumes.

Completed measurements: all six variants on macOS arm64, Windows AMD64 and Linux
aarch64/x86_64. All available wheel tests pass. Saved reports are under
artifacts/report-38309369474 locally; that report excludes the final x86_64 PR
baseline, now downloaded under artifacts/run-38309406995. The revised comment
includes this final result and presents percentage growth against no-jxl.

Outstanding runs at pause:

- macOS Intel common dependencies and six variants: 38306998901.

Successful build artifact sources for a combined report:

- macOS arm64: 38304925834.
- Windows: 38306989036.
- Linux aarch64 and five Linux x86_64 variants: 38308512861.
- Linux x86_64 PR: 38309406995, if successful.
- macOS Intel: 38306998901, if successful.

Latest report: 38309369474. New report.yml additionally preserves raw measurement
JSON and JUnit XML, allowing them to be committed for durable evidence after all
builds finish. Avoid compiling successful variants again. A report workflow can
combine comma-separated source run IDs without building anything.

Controlled comparisons: 38308643532 (macOS arm64), 38308639837 (Windows).
Downloaded under artifacts/controlled-*. Decoder/minsize/LTO exactly match PR
sample pixels on the same host. Cross-runner Windows hash differences disappear
on the same host. Scalar changes some 8-bit channel values by at most one and
slows flower decoding substantially. Windows size optimization also slows these
samples; macOS LTO is close to PR. Hosted benchmark limits still apply.

Harness repairs already published: portable checksum code for older container
Python, host export for Linux archives, Windows cwd restoration, rsync installed
before capturing fetch_unpack stdout, and PR standalone tools disabled to avoid
a Linux x86_64 libsharpyuv PIE benchmark link failure. Library settings remain
the PR's for that baseline. Reuse saved common artifacts for any further retry.

Local checks passed: scripts/check_pipeline.py, Python syntax, new workflow YAML.
Root Git requires -c safe.directory=C:/Users/Ewout/Documents/GitHub/jpeg-xl-wheel-size.
The untracked root RESULTS.md is an older partial report; regenerate before use.
