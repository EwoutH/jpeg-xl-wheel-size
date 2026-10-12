# Same-runner decoding comparison

Host: `Linux-6.17.0-1022-azure-x86_64-with-glibc2.39` / `x86_64`

All wheels run sequentially on the same host in separate Python processes. This removes cross-runner CPU differences, but does not control thermals or shared-host load. Timing ratios are sample medians, not release performance guarantees.

| Variant | Sample | Maximum channel difference | Changed channel values | Decode time vs PR |
| --- | --- | ---: | ---: | ---: |
| pr | hopper.jxl | 0 | 0/49152 | 1.00 |
| pr | hopper_gray.jxl | 0 | 0/16384 | 1.00 |
| pr | transparent.jxl | 0 | 0/120000 | 1.00 |
| pr | flower.jxl | 0 | 0/518400 | 1.00 |
| pr | flower2.jxl | 0 | 0/202500 | 1.00 |
| pr | 16bit_subcutaneous.cropped.jxl | 0 | 0/8192 | 1.00 |
| decoder | hopper.jxl | 0 | 0/49152 | 0.98 |
| decoder | hopper_gray.jxl | 0 | 0/16384 | 1.00 |
| decoder | transparent.jxl | 0 | 0/120000 | 1.02 |
| decoder | flower.jxl | 0 | 0/518400 | 1.00 |
| decoder | flower2.jxl | 0 | 0/202500 | 1.02 |
| decoder | 16bit_subcutaneous.cropped.jxl | 0 | 0/8192 | 1.00 |
| minsize | hopper.jxl | 1 | 1/49152 | 1.05 |
| minsize | hopper_gray.jxl | 0 | 0/16384 | 1.07 |
| minsize | transparent.jxl | 0 | 0/120000 | 1.10 |
| minsize | flower.jxl | 1 | 4/518400 | 1.06 |
| minsize | flower2.jxl | 1 | 1/202500 | 1.08 |
| minsize | 16bit_subcutaneous.cropped.jxl | 0 | 0/8192 | 1.07 |
| lto | hopper.jxl | 1 | 1/49152 | 1.06 |
| lto | hopper_gray.jxl | 0 | 0/16384 | 1.06 |
| lto | transparent.jxl | 0 | 0/120000 | 1.07 |
| lto | flower.jxl | 1 | 4/518400 | 1.09 |
| lto | flower2.jxl | 1 | 1/202500 | 1.10 |
| lto | 16bit_subcutaneous.cropped.jxl | 0 | 0/8192 | 1.05 |
| scalar | hopper.jxl | 1 | 736/49152 | 2.02 |
| scalar | hopper_gray.jxl | 1 | 218/16384 | 1.74 |
| scalar | transparent.jxl | 0 | 0/120000 | 1.13 |
| scalar | flower.jxl | 1 | 8132/518400 | 3.79 |
| scalar | flower2.jxl | 1 | 3027/202500 | 3.78 |
| scalar | 16bit_subcutaneous.cropped.jxl | 0 | 0/8192 | 1.11 |
