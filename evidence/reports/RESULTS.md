# Measured wheel sizes

Sizes are MiB (1,048,576 bytes). Comparisons use the same Pillow commit and CPython ABI.

| Platform | Variant | Wheel MiB | Installed MiB | vs PR | JPEG XL overhead vs disabled |
| --- | --- | ---: | ---: | ---: | ---: |
| linux-aarch64 | no-jxl | 6.409 | 20.422 | -19.87% | +0.000 MiB (+0.00%) |
| linux-aarch64 | pr | 7.998 | 25.317 | +0.00% | +1.589 MiB (+24.79%) |
| linux-aarch64 | decoder | 6.934 | 22.434 | -13.31% | +0.525 MiB (+8.19%) |
| linux-aarch64 | minsize | 6.771 | 22.060 | -15.34% | +0.362 MiB (+5.65%) |
| linux-aarch64 | lto | 6.717 | 21.872 | -16.02% | +0.307 MiB (+4.80%) |
| linux-aarch64 | scalar | 6.705 | 21.810 | -16.17% | +0.296 MiB (+4.61%) |
| linux-x86_64 | no-jxl | 6.971 | 19.380 | -22.98% | +0.000 MiB (+0.00%) |
| linux-x86_64 | pr | 9.052 | 24.654 | +0.00% | +2.080 MiB (+29.84%) |
| linux-x86_64 | decoder | 7.676 | 21.212 | -15.20% | +0.704 MiB (+10.10%) |
| linux-x86_64 | minsize | 7.435 | 20.642 | -17.87% | +0.463 MiB (+6.64%) |
| linux-x86_64 | lto | 7.357 | 20.404 | -18.72% | +0.386 MiB (+5.53%) |
| linux-x86_64 | scalar | 7.262 | 20.111 | -19.77% | +0.291 MiB (+4.17%) |
| macos-arm64 | no-jxl | 4.565 | 11.362 | -22.56% | +0.000 MiB (+0.00%) |
| macos-arm64 | pr | 5.894 | 14.804 | +0.00% | +1.330 MiB (+29.13%) |
| macos-arm64 | decoder | 4.993 | 12.624 | -15.29% | +0.429 MiB (+9.39%) |
| macos-arm64 | minsize | 4.885 | 12.382 | -17.12% | +0.321 MiB (+7.03%) |
| macos-arm64 | lto | 4.835 | 12.182 | -17.97% | +0.270 MiB (+5.92%) |
| macos-arm64 | scalar | 4.814 | 12.081 | -18.33% | +0.249 MiB (+5.45%) |
| macos-x86_64 | no-jxl | 5.283 | 12.848 | -29.03% | +0.000 MiB (+0.00%) |
| macos-x86_64 | pr | 7.443 | 18.880 | +0.00% | +2.161 MiB (+40.91%) |
| macos-x86_64 | decoder | 5.970 | 14.961 | -19.80% | +0.687 MiB (+13.01%) |
| macos-x86_64 | minsize | 5.759 | 14.384 | -22.63% | +0.476 MiB (+9.01%) |
| macos-x86_64 | lto | 5.680 | 14.021 | -23.70% | +0.397 MiB (+7.52%) |
| macos-x86_64 | scalar | 5.557 | 13.530 | -25.35% | +0.274 MiB (+5.19%) |
| windows-amd64 | no-jxl | 6.793 | 14.063 | -7.81% | +0.000 MiB (+0.00%) |
| windows-amd64 | pr | 7.368 | 15.477 | +0.00% | +0.576 MiB (+8.48%) |
| windows-amd64 | decoder | 7.368 | 15.477 | -0.00% | +0.576 MiB (+8.48%) |
| windows-amd64 | minsize | 7.262 | 15.212 | -1.44% | +0.470 MiB (+6.92%) |
| windows-amd64 | lto | 7.262 | 15.183 | -1.44% | +0.470 MiB (+6.92%) |
| windows-amd64 | scalar | 7.188 | 14.932 | -2.45% | +0.396 MiB (+5.82%) |

## Decoding checks

The workflow asserts JPEG XL availability and runs selftest plus the JPEG XL, JPEG and PNG tests. Pixel hashes below compare each variant against PR on the same architecture. A hash difference needs investigation; matching hashes cover these samples only.

- linux-aarch64 / pr: pixel hashes match; sum of sample median decode times 1.00× PR.
- linux-aarch64 / decoder: pixel hashes match; sum of sample median decode times 1.04× PR.
- linux-aarch64 / minsize: pixel hashes match; sum of sample median decode times 1.10× PR.
- linux-aarch64 / lto: pixel hashes match; sum of sample median decode times 1.09× PR.
- linux-aarch64 / scalar: pixel hashes DIFFER; sum of sample median decode times 1.94× PR.
  Differing samples: hopper.jxl, hopper_gray.jxl, flower.jxl, flower2.jxl.
- linux-x86_64 / pr: pixel hashes match; sum of sample median decode times 1.00× PR.
- linux-x86_64 / decoder: pixel hashes match; sum of sample median decode times 1.00× PR.
- linux-x86_64 / minsize: pixel hashes DIFFER; sum of sample median decode times 1.09× PR.
  Differing samples: hopper.jxl, flower.jxl, flower2.jxl.
- linux-x86_64 / lto: pixel hashes DIFFER; sum of sample median decode times 1.14× PR.
  Differing samples: flower.jxl, flower2.jxl.
- linux-x86_64 / scalar: pixel hashes DIFFER; sum of sample median decode times 2.36× PR.
  Differing samples: hopper.jxl, hopper_gray.jxl, flower.jxl, flower2.jxl.
- macos-arm64 / pr: pixel hashes match; sum of sample median decode times 1.00× PR.
- macos-arm64 / decoder: pixel hashes match; sum of sample median decode times 1.23× PR.
- macos-arm64 / minsize: pixel hashes match; sum of sample median decode times 1.50× PR.
- macos-arm64 / lto: pixel hashes match; sum of sample median decode times 1.42× PR.
- macos-arm64 / scalar: pixel hashes DIFFER; sum of sample median decode times 2.70× PR.
  Differing samples: hopper.jxl, hopper_gray.jxl, flower.jxl, flower2.jxl.
- macos-x86_64 / pr: pixel hashes match; sum of sample median decode times 1.00× PR.
- macos-x86_64 / decoder: pixel hashes match; sum of sample median decode times 1.19× PR.
- macos-x86_64 / minsize: pixel hashes match; sum of sample median decode times 1.57× PR.
- macos-x86_64 / lto: pixel hashes match; sum of sample median decode times 0.89× PR.
- macos-x86_64 / scalar: pixel hashes DIFFER; sum of sample median decode times 1.39× PR.
  Differing samples: hopper.jxl, hopper_gray.jxl, flower.jxl, flower2.jxl.
- windows-amd64 / pr: pixel hashes match; sum of sample median decode times 1.00× PR.
- windows-amd64 / decoder: pixel hashes DIFFER; sum of sample median decode times 1.25× PR.
  Differing samples: flower.jxl, flower2.jxl.
- windows-amd64 / minsize: pixel hashes DIFFER; sum of sample median decode times 1.47× PR.
  Differing samples: flower.jxl, flower2.jxl.
- windows-amd64 / lto: pixel hashes DIFFER; sum of sample median decode times 1.55× PR.
  Differing samples: flower.jxl, flower2.jxl.
- windows-amd64 / scalar: pixel hashes DIFFER; sum of sample median decode times 2.34× PR.
  Differing samples: hopper.jxl, hopper_gray.jxl, flower.jxl, flower2.jxl.

Hosted runners differ: timing ratios are exploratory, not controlled performance benchmarks.

## Saved pytest results

Counts include optional-dependency skips. Availability assertions and Pillow selftest are separate workflow steps.

| Artifact | Tests | Failures | Errors | Skipped |
| --- | ---: | ---: | ---: | ---: |
| tests-linux-aarch64-decoder | 196 | 0 | 0 | 2 |
| tests-linux-aarch64-lto | 196 | 0 | 0 | 2 |
| tests-linux-aarch64-minsize | 196 | 0 | 0 | 2 |
| tests-linux-aarch64-no-jxl | 196 | 0 | 0 | 20 |
| tests-linux-aarch64-pr | 196 | 0 | 0 | 2 |
| tests-linux-aarch64-scalar | 196 | 0 | 0 | 2 |
| tests-linux-x86_64-decoder | 196 | 0 | 0 | 2 |
| tests-linux-x86_64-lto | 196 | 0 | 0 | 2 |
| tests-linux-x86_64-minsize | 196 | 0 | 0 | 2 |
| tests-linux-x86_64-no-jxl | 196 | 0 | 0 | 20 |
| tests-linux-x86_64-pr | 196 | 0 | 0 | 2 |
| tests-linux-x86_64-scalar | 196 | 0 | 0 | 2 |
| tests-macos-arm64-decoder | 196 | 0 | 0 | 1 |
| tests-macos-arm64-lto | 196 | 0 | 0 | 1 |
| tests-macos-arm64-minsize | 196 | 0 | 0 | 1 |
| tests-macos-arm64-no-jxl | 196 | 0 | 0 | 19 |
| tests-macos-arm64-pr | 196 | 0 | 0 | 1 |
| tests-macos-arm64-scalar | 196 | 0 | 0 | 1 |
| tests-macos-x86_64-decoder | 196 | 0 | 0 | 1 |
| tests-macos-x86_64-lto | 196 | 0 | 0 | 1 |
| tests-macos-x86_64-minsize | 196 | 0 | 0 | 1 |
| tests-macos-x86_64-no-jxl | 196 | 0 | 0 | 19 |
| tests-macos-x86_64-pr | 196 | 0 | 0 | 1 |
| tests-macos-x86_64-scalar | 196 | 0 | 0 | 1 |
| tests-windows-amd64-decoder | 196 | 0 | 0 | 2 |
| tests-windows-amd64-lto | 196 | 0 | 0 | 2 |
| tests-windows-amd64-minsize | 196 | 0 | 0 | 2 |
| tests-windows-amd64-no-jxl | 196 | 0 | 0 | 20 |
| tests-windows-amd64-pr | 196 | 0 | 0 | 2 |
| tests-windows-amd64-scalar | 196 | 0 | 0 | 2 |

## ZIP compression level 9

Repacked wheel contents are byte-for-byte identical, including RECORD. Installed size is unchanged.

| Wheel | Saved KiB | Saved % |
| --- | ---: | ---: |
| run-38308512861/wheel-linux-aarch64-decoder/wheelhouse/pillow-13.0.0.dev0-cp313-cp313-manylinux_2_27_aarch64.manylinux_2_28_aarch64.whl | 258.5 | 3.64% |
| run-38308512861/wheel-linux-aarch64-lto/wheelhouse/pillow-13.0.0.dev0-cp313-cp313-manylinux_2_27_aarch64.manylinux_2_28_aarch64.whl | 249.4 | 3.63% |
| run-38308512861/wheel-linux-aarch64-minsize/wheelhouse/pillow-13.0.0.dev0-cp313-cp313-manylinux_2_27_aarch64.manylinux_2_28_aarch64.whl | 253.4 | 3.65% |
| run-38308512861/wheel-linux-aarch64-no-jxl/wheelhouse/pillow-13.0.0.dev0-cp313-cp313-manylinux_2_27_aarch64.manylinux_2_28_aarch64.whl | 236.3 | 3.60% |
| run-38308512861/wheel-linux-aarch64-pr/wheelhouse/pillow-13.0.0.dev0-cp313-cp313-manylinux_2_27_aarch64.manylinux_2_28_aarch64.whl | 298.2 | 3.64% |
| run-38308512861/wheel-linux-aarch64-scalar/wheelhouse/pillow-13.0.0.dev0-cp313-cp313-manylinux_2_27_aarch64.manylinux_2_28_aarch64.whl | 247.1 | 3.60% |
| run-38308512861/wheel-linux-x86_64-decoder/wheelhouse/pillow-13.0.0.dev0-cp313-cp313-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl | 237.7 | 3.02% |
| run-38308512861/wheel-linux-x86_64-lto/wheelhouse/pillow-13.0.0.dev0-cp313-cp313-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl | 229.1 | 3.04% |
| run-38308512861/wheel-linux-x86_64-minsize/wheelhouse/pillow-13.0.0.dev0-cp313-cp313-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl | 233.6 | 3.07% |
| run-38308512861/wheel-linux-x86_64-no-jxl/wheelhouse/pillow-13.0.0.dev0-cp313-cp313-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl | 212.2 | 2.97% |
| run-38309406995/wheel-linux-x86_64-pr/wheelhouse/pillow-13.0.0.dev0-cp313-cp313-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl | 279.6 | 3.02% |
| run-38308512861/wheel-linux-x86_64-scalar/wheelhouse/pillow-13.0.0.dev0-cp313-cp313-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl | 222.9 | 3.00% |
| run-38304925834/wheel-macos-arm64-decoder/wheelhouse/pillow-13.0.0.dev0-cp313-cp313-macosx_11_0_arm64.whl | 7.1 | 0.14% |
| run-38304925834/wheel-macos-arm64-lto/wheelhouse/pillow-13.0.0.dev0-cp313-cp313-macosx_11_0_arm64.whl | 7.0 | 0.14% |
| run-38304925834/wheel-macos-arm64-minsize/wheelhouse/pillow-13.0.0.dev0-cp313-cp313-macosx_11_0_arm64.whl | 7.2 | 0.14% |
| run-38304925834/wheel-macos-arm64-no-jxl/wheelhouse/pillow-13.0.0.dev0-cp313-cp313-macosx_11_0_arm64.whl | 6.6 | 0.14% |
| run-38304925834/wheel-macos-arm64-pr/wheelhouse/pillow-13.0.0.dev0-cp313-cp313-macosx_11_0_arm64.whl | 8.6 | 0.14% |
| run-38304925834/wheel-macos-arm64-scalar/wheelhouse/pillow-13.0.0.dev0-cp313-cp313-macosx_11_0_arm64.whl | 6.9 | 0.14% |
| run-38306998901/wheel-macos-x86_64-decoder/wheelhouse/pillow-13.0.0.dev0-cp313-cp313-macosx_10_13_x86_64.whl | 16.1 | 0.26% |
| run-38306998901/wheel-macos-x86_64-lto/wheelhouse/pillow-13.0.0.dev0-cp313-cp313-macosx_10_13_x86_64.whl | 12.9 | 0.22% |
| run-38306998901/wheel-macos-x86_64-minsize/wheelhouse/pillow-13.0.0.dev0-cp313-cp313-macosx_10_13_x86_64.whl | 14.0 | 0.24% |
| run-38306998901/wheel-macos-x86_64-no-jxl/wheelhouse/pillow-13.0.0.dev0-cp313-cp313-macosx_10_13_x86_64.whl | 12.1 | 0.22% |
| run-38306998901/wheel-macos-x86_64-pr/wheelhouse/pillow-13.0.0.dev0-cp313-cp313-macosx_10_13_x86_64.whl | 25.0 | 0.33% |
| run-38306998901/wheel-macos-x86_64-scalar/wheelhouse/pillow-13.0.0.dev0-cp313-cp313-macosx_10_13_x86_64.whl | 12.6 | 0.22% |
| run-38306989036/wheel-windows-amd64-decoder/wheelhouse/pillow-13.0.0.dev0-cp313-cp313-win_amd64.whl | 16.8 | 0.22% |
| run-38306989036/wheel-windows-amd64-lto/wheelhouse/pillow-13.0.0.dev0-cp313-cp313-win_amd64.whl | 16.6 | 0.22% |
| run-38306989036/wheel-windows-amd64-minsize/wheelhouse/pillow-13.0.0.dev0-cp313-cp313-win_amd64.whl | 16.4 | 0.22% |
| run-38306989036/wheel-windows-amd64-no-jxl/wheelhouse/pillow-13.0.0.dev0-cp313-cp313-win_amd64.whl | 15.4 | 0.22% |
| run-38306989036/wheel-windows-amd64-pr/wheelhouse/pillow-13.0.0.dev0-cp313-cp313-win_amd64.whl | 16.8 | 0.22% |
| run-38306989036/wheel-windows-amd64-scalar/wheelhouse/pillow-13.0.0.dev0-cp313-cp313-win_amd64.whl | 16.4 | 0.22% |
