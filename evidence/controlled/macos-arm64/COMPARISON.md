# Same-runner decoding comparison

Host: `macOS-15.7.9-arm64-arm-64bit-Mach-O` / `arm`

All wheels run sequentially on the same host in separate Python processes. This removes cross-runner CPU differences, but does not control thermals or shared-host load. Timing ratios are sample medians, not release performance guarantees.

| Variant | Sample | Maximum channel difference | Changed channel values | Decode time vs PR |
| --- | --- | ---: | ---: | ---: |
| pr | hopper.jxl | 0 | 0/49152 | 1.00 |
| pr | hopper_gray.jxl | 0 | 0/16384 | 1.00 |
| pr | transparent.jxl | 0 | 0/120000 | 1.00 |
| pr | flower.jxl | 0 | 0/518400 | 1.00 |
| pr | flower2.jxl | 0 | 0/202500 | 1.00 |
| pr | 16bit_subcutaneous.cropped.jxl | 0 | 0/8192 | 1.00 |
| decoder | hopper.jxl | 0 | 0/49152 | 0.99 |
| decoder | hopper_gray.jxl | 0 | 0/16384 | 0.97 |
| decoder | transparent.jxl | 0 | 0/120000 | 0.91 |
| decoder | flower.jxl | 0 | 0/518400 | 0.83 |
| decoder | flower2.jxl | 0 | 0/202500 | 0.88 |
| decoder | 16bit_subcutaneous.cropped.jxl | 0 | 0/8192 | 1.01 |
| minsize | hopper.jxl | 0 | 0/49152 | 0.98 |
| minsize | hopper_gray.jxl | 0 | 0/16384 | 1.03 |
| minsize | transparent.jxl | 0 | 0/120000 | 0.99 |
| minsize | flower.jxl | 0 | 0/518400 | 1.24 |
| minsize | flower2.jxl | 0 | 0/202500 | 1.03 |
| minsize | 16bit_subcutaneous.cropped.jxl | 0 | 0/8192 | 1.03 |
| lto | hopper.jxl | 0 | 0/49152 | 0.94 |
| lto | hopper_gray.jxl | 0 | 0/16384 | 0.97 |
| lto | transparent.jxl | 0 | 0/120000 | 0.93 |
| lto | flower.jxl | 0 | 0/518400 | 1.00 |
| lto | flower2.jxl | 0 | 0/202500 | 0.97 |
| lto | 16bit_subcutaneous.cropped.jxl | 0 | 0/8192 | 1.01 |
| scalar | hopper.jxl | 1 | 12/49152 | 2.17 |
| scalar | hopper_gray.jxl | 1 | 1/16384 | 1.77 |
| scalar | transparent.jxl | 0 | 0/120000 | 1.03 |
| scalar | flower.jxl | 1 | 112/518400 | 2.72 |
| scalar | flower2.jxl | 1 | 44/202500 | 3.19 |
| scalar | 16bit_subcutaneous.cropped.jxl | 0 | 0/8192 | 1.12 |
