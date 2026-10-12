# Comparisons using Pillow's own tooling

Tables use the unmodified key matching and rendering functions from Pillow's `.github/compare-dist-sizes.py` (PR #9621), at the pinned experiment commit.

The same-commit tables isolate JPEG XL. The PyPI tables also include unrelated changes since the release. Totals cover only the sampled wheel tags; they do not represent a complete Pillow release matrix.

# no-jxl

## Dist size comparison vs same-commit JPEG XL disabled

| File                                                          | Size before |    Size now |        Change |
| :-------------------------------------------------------------|-----------: |-----------: |-------------: |
| cp313-cp313-macosx_10_13_x86_64.whl                           |      5.5 MB |      5.5 MB |     🟢 +0.00% |
| cp313-cp313-macosx_11_0_arm64.whl                             |      4.8 MB |      4.8 MB |     🟢 +0.00% |
| cp313-cp313-manylinux_2_27_aarch64.manylinux_2_28_aarch64.whl |      6.7 MB |      6.7 MB |     🟢 +0.00% |
| cp313-cp313-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl   |      7.3 MB |      7.3 MB |     🟢 +0.00% |
| cp313-cp313-win_amd64.whl                                     |      7.1 MB |      7.1 MB |     🟢 +0.00% |
| **wheel average (5 wheels)**                                  |  **6.3 MB** |  **6.3 MB** | **🟢 +0.00%** |
| **wheel total (5 wheels)**                                    | **31.5 MB** | **31.5 MB** | **🟢 +0.00%** |
| **artifacts total (5 artifacts)**                             | **31.5 MB** | **31.5 MB** | **🟢 +0.00%** |

## Dist size comparison vs same-commit original JPEG XL PR

| File                                                          | Size before |    Size now |         Change |
| :-------------------------------------------------------------|-----------: |-----------: |--------------: |
| cp313-cp313-macosx_10_13_x86_64.whl                           |      7.8 MB |      5.5 MB |     🟢 -29.03% |
| cp313-cp313-macosx_11_0_arm64.whl                             |      6.2 MB |      4.8 MB |     🟢 -22.56% |
| cp313-cp313-manylinux_2_27_aarch64.manylinux_2_28_aarch64.whl |      8.4 MB |      6.7 MB |     🟢 -19.87% |
| cp313-cp313-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl   |      9.5 MB |      7.3 MB |     🟢 -22.98% |
| cp313-cp313-win_amd64.whl                                     |      7.7 MB |      7.1 MB |      🟢 -7.81% |
| **wheel average (5 wheels)**                                  |  **7.9 MB** |  **6.3 MB** | **🟢 -20.49%** |
| **wheel total (5 wheels)**                                    | **39.6 MB** | **31.5 MB** | **🟢 -20.49%** |
| **artifacts total (5 artifacts)**                             | **39.6 MB** | **31.5 MB** | **🟢 -20.49%** |

## Dist size comparison vs Pillow 12.3.0 on PyPI

| File                                                          | Size before |    Size now |        Change |
| :-------------------------------------------------------------|-----------: |-----------: |-------------: |
| cp313-cp313-macosx_10_13_x86_64.whl                           |      5.3 MB |      5.5 MB |     🟡 +3.61% |
| cp313-cp313-macosx_11_0_arm64.whl                             |      4.8 MB |      4.8 MB |     🟡 +0.13% |
| cp313-cp313-manylinux_2_27_aarch64.manylinux_2_28_aarch64.whl |      6.3 MB |      6.7 MB |     🔴 +7.29% |
| cp313-cp313-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl   |      6.9 MB |      7.3 MB |     🔴 +5.38% |
| cp313-cp313-win_amd64.whl                                     |      7.2 MB |      7.1 MB |     🟢 -1.62% |
| **wheel average (5 wheels)**                                  |  **6.1 MB** |  **6.3 MB** | **🟡 +2.98%** |
| **wheel total (5 wheels)**                                    | **30.6 MB** | **31.5 MB** | **🟡 +2.98%** |
| **artifacts total (5 artifacts)**                             | **30.6 MB** | **31.5 MB** | **🟡 +2.98%** |

# pr

## Dist size comparison vs same-commit JPEG XL disabled

| File                                                          | Size before |    Size now |         Change |
| :-------------------------------------------------------------|-----------: |-----------: |--------------: |
| cp313-cp313-macosx_10_13_x86_64.whl                           |      5.5 MB |      7.8 MB |     🔴 +40.91% |
| cp313-cp313-macosx_11_0_arm64.whl                             |      4.8 MB |      6.2 MB |     🔴 +29.13% |
| cp313-cp313-manylinux_2_27_aarch64.manylinux_2_28_aarch64.whl |      6.7 MB |      8.4 MB |     🔴 +24.79% |
| cp313-cp313-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl   |      7.3 MB |      9.5 MB |     🔴 +29.84% |
| cp313-cp313-win_amd64.whl                                     |      7.1 MB |      7.7 MB |      🔴 +8.48% |
| **wheel average (5 wheels)**                                  |  **6.3 MB** |  **7.9 MB** | **🔴 +25.77%** |
| **wheel total (5 wheels)**                                    | **31.5 MB** | **39.6 MB** | **🔴 +25.77%** |
| **artifacts total (5 artifacts)**                             | **31.5 MB** | **39.6 MB** | **🔴 +25.77%** |

## Dist size comparison vs same-commit original JPEG XL PR

| File                                                          | Size before |    Size now |        Change |
| :-------------------------------------------------------------|-----------: |-----------: |-------------: |
| cp313-cp313-macosx_10_13_x86_64.whl                           |      7.8 MB |      7.8 MB |     🟢 +0.00% |
| cp313-cp313-macosx_11_0_arm64.whl                             |      6.2 MB |      6.2 MB |     🟢 +0.00% |
| cp313-cp313-manylinux_2_27_aarch64.manylinux_2_28_aarch64.whl |      8.4 MB |      8.4 MB |     🟢 +0.00% |
| cp313-cp313-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl   |      9.5 MB |      9.5 MB |     🟢 +0.00% |
| cp313-cp313-win_amd64.whl                                     |      7.7 MB |      7.7 MB |     🟢 +0.00% |
| **wheel average (5 wheels)**                                  |  **7.9 MB** |  **7.9 MB** | **🟢 +0.00%** |
| **wheel total (5 wheels)**                                    | **39.6 MB** | **39.6 MB** | **🟢 +0.00%** |
| **artifacts total (5 artifacts)**                             | **39.6 MB** | **39.6 MB** | **🟢 +0.00%** |

## Dist size comparison vs Pillow 12.3.0 on PyPI

| File                                                          | Size before |    Size now |         Change |
| :-------------------------------------------------------------|-----------: |-----------: |--------------: |
| cp313-cp313-macosx_10_13_x86_64.whl                           |      5.3 MB |      7.8 MB |     🔴 +46.00% |
| cp313-cp313-macosx_11_0_arm64.whl                             |      4.8 MB |      6.2 MB |     🔴 +29.30% |
| cp313-cp313-manylinux_2_27_aarch64.manylinux_2_28_aarch64.whl |      6.3 MB |      8.4 MB |     🔴 +33.89% |
| cp313-cp313-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl   |      6.9 MB |      9.5 MB |     🔴 +36.82% |
| cp313-cp313-win_amd64.whl                                     |      7.2 MB |      7.7 MB |      🔴 +6.72% |
| **wheel average (5 wheels)**                                  |  **6.1 MB** |  **7.9 MB** | **🔴 +29.52%** |
| **wheel total (5 wheels)**                                    | **30.6 MB** | **39.6 MB** | **🔴 +29.52%** |
| **artifacts total (5 artifacts)**                             | **30.6 MB** | **39.6 MB** | **🔴 +29.52%** |

# decoder

## Dist size comparison vs same-commit JPEG XL disabled

| File                                                          | Size before |    Size now |        Change |
| :-------------------------------------------------------------|-----------: |-----------: |-------------: |
| cp313-cp313-macosx_10_13_x86_64.whl                           |      5.5 MB |      6.3 MB |    🔴 +13.01% |
| cp313-cp313-macosx_11_0_arm64.whl                             |      4.8 MB |      5.2 MB |     🔴 +9.39% |
| cp313-cp313-manylinux_2_27_aarch64.manylinux_2_28_aarch64.whl |      6.7 MB |      7.3 MB |     🔴 +8.19% |
| cp313-cp313-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl   |      7.3 MB |      8.0 MB |    🔴 +10.10% |
| cp313-cp313-win_amd64.whl                                     |      7.1 MB |      7.7 MB |     🔴 +8.48% |
| **wheel average (5 wheels)**                                  |  **6.3 MB** |  **6.9 MB** | **🔴 +9.73%** |
| **wheel total (5 wheels)**                                    | **31.5 MB** | **34.5 MB** | **🔴 +9.73%** |
| **artifacts total (5 artifacts)**                             | **31.5 MB** | **34.5 MB** | **🔴 +9.73%** |

## Dist size comparison vs same-commit original JPEG XL PR

| File                                                          | Size before |    Size now |         Change |
| :-------------------------------------------------------------|-----------: |-----------: |--------------: |
| cp313-cp313-macosx_10_13_x86_64.whl                           |      7.8 MB |      6.3 MB |     🟢 -19.80% |
| cp313-cp313-macosx_11_0_arm64.whl                             |      6.2 MB |      5.2 MB |     🟢 -15.29% |
| cp313-cp313-manylinux_2_27_aarch64.manylinux_2_28_aarch64.whl |      8.4 MB |      7.3 MB |     🟢 -13.31% |
| cp313-cp313-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl   |      9.5 MB |      8.0 MB |     🟢 -15.20% |
| cp313-cp313-win_amd64.whl                                     |      7.7 MB |      7.7 MB |      🟢 -0.00% |
| **wheel average (5 wheels)**                                  |  **7.9 MB** |  **6.9 MB** | **🟢 -12.75%** |
| **wheel total (5 wheels)**                                    | **39.6 MB** | **34.5 MB** | **🟢 -12.75%** |
| **artifacts total (5 artifacts)**                             | **39.6 MB** | **34.5 MB** | **🟢 -12.75%** |

## Dist size comparison vs Pillow 12.3.0 on PyPI

| File                                                          | Size before |    Size now |         Change |
| :-------------------------------------------------------------|-----------: |-----------: |--------------: |
| cp313-cp313-macosx_10_13_x86_64.whl                           |      5.3 MB |      6.3 MB |     🔴 +17.10% |
| cp313-cp313-macosx_11_0_arm64.whl                             |      4.8 MB |      5.2 MB |      🔴 +9.53% |
| cp313-cp313-manylinux_2_27_aarch64.manylinux_2_28_aarch64.whl |      6.3 MB |      7.3 MB |     🔴 +16.08% |
| cp313-cp313-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl   |      6.9 MB |      8.0 MB |     🔴 +16.02% |
| cp313-cp313-win_amd64.whl                                     |      7.2 MB |      7.7 MB |      🔴 +6.72% |
| **wheel average (5 wheels)**                                  |  **6.1 MB** |  **6.9 MB** | **🔴 +13.00%** |
| **wheel total (5 wheels)**                                    | **30.6 MB** | **34.5 MB** | **🔴 +13.00%** |
| **artifacts total (5 artifacts)**                             | **30.6 MB** | **34.5 MB** | **🔴 +13.00%** |

# minsize

## Dist size comparison vs same-commit JPEG XL disabled

| File                                                          | Size before |    Size now |        Change |
| :-------------------------------------------------------------|-----------: |-----------: |-------------: |
| cp313-cp313-macosx_10_13_x86_64.whl                           |      5.5 MB |      6.0 MB |     🔴 +9.01% |
| cp313-cp313-macosx_11_0_arm64.whl                             |      4.8 MB |      5.1 MB |     🔴 +7.03% |
| cp313-cp313-manylinux_2_27_aarch64.manylinux_2_28_aarch64.whl |      6.7 MB |      7.1 MB |     🔴 +5.65% |
| cp313-cp313-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl   |      7.3 MB |      7.8 MB |     🔴 +6.64% |
| cp313-cp313-win_amd64.whl                                     |      7.1 MB |      7.6 MB |     🔴 +6.92% |
| **wheel average (5 wheels)**                                  |  **6.3 MB** |  **6.7 MB** | **🔴 +6.97%** |
| **wheel total (5 wheels)**                                    | **31.5 MB** | **33.7 MB** | **🔴 +6.97%** |
| **artifacts total (5 artifacts)**                             | **31.5 MB** | **33.7 MB** | **🔴 +6.97%** |

## Dist size comparison vs same-commit original JPEG XL PR

| File                                                          | Size before |    Size now |         Change |
| :-------------------------------------------------------------|-----------: |-----------: |--------------: |
| cp313-cp313-macosx_10_13_x86_64.whl                           |      7.8 MB |      6.0 MB |     🟢 -22.63% |
| cp313-cp313-macosx_11_0_arm64.whl                             |      6.2 MB |      5.1 MB |     🟢 -17.12% |
| cp313-cp313-manylinux_2_27_aarch64.manylinux_2_28_aarch64.whl |      8.4 MB |      7.1 MB |     🟢 -15.34% |
| cp313-cp313-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl   |      9.5 MB |      7.8 MB |     🟢 -17.87% |
| cp313-cp313-win_amd64.whl                                     |      7.7 MB |      7.6 MB |      🟢 -1.44% |
| **wheel average (5 wheels)**                                  |  **7.9 MB** |  **6.7 MB** | **🟢 -14.95%** |
| **wheel total (5 wheels)**                                    | **39.6 MB** | **33.7 MB** | **🟢 -14.95%** |
| **artifacts total (5 artifacts)**                             | **39.6 MB** | **33.7 MB** | **🟢 -14.95%** |

## Dist size comparison vs Pillow 12.3.0 on PyPI

| File                                                          | Size before |    Size now |         Change |
| :-------------------------------------------------------------|-----------: |-----------: |--------------: |
| cp313-cp313-macosx_10_13_x86_64.whl                           |      5.3 MB |      6.0 MB |     🔴 +12.95% |
| cp313-cp313-macosx_11_0_arm64.whl                             |      4.8 MB |      5.1 MB |      🔴 +7.17% |
| cp313-cp313-manylinux_2_27_aarch64.manylinux_2_28_aarch64.whl |      6.3 MB |      7.1 MB |     🔴 +13.35% |
| cp313-cp313-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl   |      6.9 MB |      7.8 MB |     🔴 +12.38% |
| cp313-cp313-win_amd64.whl                                     |      7.2 MB |      7.6 MB |      🔴 +5.19% |
| **wheel average (5 wheels)**                                  |  **6.1 MB** |  **6.7 MB** | **🔴 +10.16%** |
| **wheel total (5 wheels)**                                    | **30.6 MB** | **33.7 MB** | **🔴 +10.16%** |
| **artifacts total (5 artifacts)**                             | **30.6 MB** | **33.7 MB** | **🔴 +10.16%** |

# lto

## Dist size comparison vs same-commit JPEG XL disabled

| File                                                          | Size before |    Size now |        Change |
| :-------------------------------------------------------------|-----------: |-----------: |-------------: |
| cp313-cp313-macosx_10_13_x86_64.whl                           |      5.5 MB |      6.0 MB |     🔴 +7.52% |
| cp313-cp313-macosx_11_0_arm64.whl                             |      4.8 MB |      5.1 MB |     🔴 +5.92% |
| cp313-cp313-manylinux_2_27_aarch64.manylinux_2_28_aarch64.whl |      6.7 MB |      7.0 MB |     🟡 +4.80% |
| cp313-cp313-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl   |      7.3 MB |      7.7 MB |     🔴 +5.53% |
| cp313-cp313-win_amd64.whl                                     |      7.1 MB |      7.6 MB |     🔴 +6.92% |
| **wheel average (5 wheels)**                                  |  **6.3 MB** |  **6.7 MB** | **🔴 +6.10%** |
| **wheel total (5 wheels)**                                    | **31.5 MB** | **33.4 MB** | **🔴 +6.10%** |
| **artifacts total (5 artifacts)**                             | **31.5 MB** | **33.4 MB** | **🔴 +6.10%** |

## Dist size comparison vs same-commit original JPEG XL PR

| File                                                          | Size before |    Size now |         Change |
| :-------------------------------------------------------------|-----------: |-----------: |--------------: |
| cp313-cp313-macosx_10_13_x86_64.whl                           |      7.8 MB |      6.0 MB |     🟢 -23.70% |
| cp313-cp313-macosx_11_0_arm64.whl                             |      6.2 MB |      5.1 MB |     🟢 -17.97% |
| cp313-cp313-manylinux_2_27_aarch64.manylinux_2_28_aarch64.whl |      8.4 MB |      7.0 MB |     🟢 -16.02% |
| cp313-cp313-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl   |      9.5 MB |      7.7 MB |     🟢 -18.72% |
| cp313-cp313-win_amd64.whl                                     |      7.7 MB |      7.6 MB |      🟢 -1.44% |
| **wheel average (5 wheels)**                                  |  **7.9 MB** |  **6.7 MB** | **🟢 -15.64%** |
| **wheel total (5 wheels)**                                    | **39.6 MB** | **33.4 MB** | **🟢 -15.64%** |
| **artifacts total (5 artifacts)**                             | **39.6 MB** | **33.4 MB** | **🟢 -15.64%** |

## Dist size comparison vs Pillow 12.3.0 on PyPI

| File                                                          | Size before |    Size now |        Change |
| :-------------------------------------------------------------|-----------: |-----------: |-------------: |
| cp313-cp313-macosx_10_13_x86_64.whl                           |      5.3 MB |      6.0 MB |    🔴 +11.40% |
| cp313-cp313-macosx_11_0_arm64.whl                             |      4.8 MB |      5.1 MB |     🔴 +6.06% |
| cp313-cp313-manylinux_2_27_aarch64.manylinux_2_28_aarch64.whl |      6.3 MB |      7.0 MB |    🔴 +12.44% |
| cp313-cp313-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl   |      6.9 MB |      7.7 MB |    🔴 +11.21% |
| cp313-cp313-win_amd64.whl                                     |      7.2 MB |      7.6 MB |     🔴 +5.19% |
| **wheel average (5 wheels)**                                  |  **6.1 MB** |  **6.7 MB** | **🔴 +9.26%** |
| **wheel total (5 wheels)**                                    | **30.6 MB** | **33.4 MB** | **🔴 +9.26%** |
| **artifacts total (5 artifacts)**                             | **30.6 MB** | **33.4 MB** | **🔴 +9.26%** |

# scalar

## Dist size comparison vs same-commit JPEG XL disabled

| File                                                          | Size before |    Size now |        Change |
| :-------------------------------------------------------------|-----------: |-----------: |-------------: |
| cp313-cp313-macosx_10_13_x86_64.whl                           |      5.5 MB |      5.8 MB |     🔴 +5.19% |
| cp313-cp313-macosx_11_0_arm64.whl                             |      4.8 MB |      5.0 MB |     🔴 +5.45% |
| cp313-cp313-manylinux_2_27_aarch64.manylinux_2_28_aarch64.whl |      6.7 MB |      7.0 MB |     🟡 +4.61% |
| cp313-cp313-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl   |      7.3 MB |      7.6 MB |     🟡 +4.17% |
| cp313-cp313-win_amd64.whl                                     |      7.1 MB |      7.5 MB |     🔴 +5.82% |
| **wheel average (5 wheels)**                                  |  **6.3 MB** |  **6.6 MB** | **🔴 +5.01%** |
| **wheel total (5 wheels)**                                    | **31.5 MB** | **33.1 MB** | **🔴 +5.01%** |
| **artifacts total (5 artifacts)**                             | **31.5 MB** | **33.1 MB** | **🔴 +5.01%** |

## Dist size comparison vs same-commit original JPEG XL PR

| File                                                          | Size before |    Size now |         Change |
| :-------------------------------------------------------------|-----------: |-----------: |--------------: |
| cp313-cp313-macosx_10_13_x86_64.whl                           |      7.8 MB |      5.8 MB |     🟢 -25.35% |
| cp313-cp313-macosx_11_0_arm64.whl                             |      6.2 MB |      5.0 MB |     🟢 -18.33% |
| cp313-cp313-manylinux_2_27_aarch64.manylinux_2_28_aarch64.whl |      8.4 MB |      7.0 MB |     🟢 -16.17% |
| cp313-cp313-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl   |      9.5 MB |      7.6 MB |     🟢 -19.77% |
| cp313-cp313-win_amd64.whl                                     |      7.7 MB |      7.5 MB |      🟢 -2.45% |
| **wheel average (5 wheels)**                                  |  **7.9 MB** |  **6.6 MB** | **🟢 -16.50%** |
| **wheel total (5 wheels)**                                    | **39.6 MB** | **33.1 MB** | **🟢 -16.50%** |
| **artifacts total (5 artifacts)**                             | **39.6 MB** | **33.1 MB** | **🟢 -16.50%** |

## Dist size comparison vs Pillow 12.3.0 on PyPI

| File                                                          | Size before |    Size now |        Change |
| :-------------------------------------------------------------|-----------: |-----------: |-------------: |
| cp313-cp313-macosx_10_13_x86_64.whl                           |      5.3 MB |      5.8 MB |     🔴 +8.99% |
| cp313-cp313-macosx_11_0_arm64.whl                             |      4.8 MB |      5.0 MB |     🔴 +5.59% |
| cp313-cp313-manylinux_2_27_aarch64.manylinux_2_28_aarch64.whl |      6.3 MB |      7.0 MB |    🔴 +12.24% |
| cp313-cp313-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl   |      6.9 MB |      7.6 MB |     🔴 +9.77% |
| cp313-cp313-win_amd64.whl                                     |      7.2 MB |      7.5 MB |     🟡 +4.11% |
| **wheel average (5 wheels)**                                  |  **6.1 MB** |  **6.6 MB** | **🔴 +8.15%** |
| **wheel total (5 wheels)**                                    | **30.6 MB** | **33.1 MB** | **🔴 +8.15%** |
| **artifacts total (5 artifacts)**                             | **30.6 MB** | **33.1 MB** | **🔴 +8.15%** |
