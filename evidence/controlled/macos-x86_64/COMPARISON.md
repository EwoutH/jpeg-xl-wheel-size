# Same-runner decoding comparison

Host: `macOS-15.7.9-x86_64-i386-64bit-Mach-O` / `i386`

All wheels run sequentially on the same host in separate Python processes. This removes cross-runner CPU differences, but does not control thermals or shared-host load. Timing ratios are sample medians, not release performance guarantees.

| Variant | Sample | Maximum channel difference | Changed channel values | Decode time vs PR |
| --- | --- | ---: | ---: | ---: |
| pr | hopper.jxl | 0 | 0/49152 | 1.00 |
| pr | hopper_gray.jxl | 0 | 0/16384 | 1.00 |
| pr | transparent.jxl | 0 | 0/120000 | 1.00 |
| pr | flower.jxl | 0 | 0/518400 | 1.00 |
| pr | flower2.jxl | 0 | 0/202500 | 1.00 |
| pr | 16bit_subcutaneous.cropped.jxl | 0 | 0/8192 | 1.00 |
| decoder | hopper.jxl | 0 | 0/49152 | 0.93 |
| decoder | hopper_gray.jxl | 0 | 0/16384 | 1.12 |
| decoder | transparent.jxl | 0 | 0/120000 | 0.75 |
| decoder | flower.jxl | 0 | 0/518400 | 0.69 |
| decoder | flower2.jxl | 0 | 0/202500 | 0.97 |
| decoder | 16bit_subcutaneous.cropped.jxl | 0 | 0/8192 | 0.92 |
| minsize | hopper.jxl | 0 | 0/49152 | 0.75 |
| minsize | hopper_gray.jxl | 0 | 0/16384 | 0.93 |
| minsize | transparent.jxl | 0 | 0/120000 | 0.70 |
| minsize | flower.jxl | 0 | 0/518400 | 0.57 |
| minsize | flower2.jxl | 0 | 0/202500 | 0.97 |
| minsize | 16bit_subcutaneous.cropped.jxl | 0 | 0/8192 | 0.80 |
| lto | hopper.jxl | 0 | 0/49152 | 0.69 |
| lto | hopper_gray.jxl | 0 | 0/16384 | 0.88 |
| lto | transparent.jxl | 0 | 0/120000 | 0.68 |
| lto | flower.jxl | 0 | 0/518400 | 0.69 |
| lto | flower2.jxl | 0 | 0/202500 | 0.97 |
| lto | 16bit_subcutaneous.cropped.jxl | 0 | 0/8192 | 0.87 |
| scalar | hopper.jxl | 1 | 736/49152 | 1.44 |
| scalar | hopper_gray.jxl | 1 | 218/16384 | 1.80 |
| scalar | transparent.jxl | 0 | 0/120000 | 0.95 |
| scalar | flower.jxl | 1 | 8124/518400 | 2.08 |
| scalar | flower2.jxl | 1 | 3026/202500 | 3.32 |
| scalar | 16bit_subcutaneous.cropped.jxl | 0 | 0/8192 | 1.10 |
