# Same-runner decoding comparison

Host: `Windows-2022Server-10.0.20348-SP0` / `AMD64 Family 25 Model 1 Stepping 1, AuthenticAMD`

All wheels run sequentially on the same host in separate Python processes. This removes cross-runner CPU differences, but does not control thermals or shared-host load. Timing ratios are sample medians, not release performance guarantees.

| Variant | Sample | Maximum channel difference | Changed channel values | Decode time vs PR |
| --- | --- | ---: | ---: | ---: |
| pr | hopper.jxl | 0 | 0/49152 | 1.00 |
| pr | hopper_gray.jxl | 0 | 0/16384 | 1.00 |
| pr | transparent.jxl | 0 | 0/120000 | 1.00 |
| pr | flower.jxl | 0 | 0/518400 | 1.00 |
| pr | flower2.jxl | 0 | 0/202500 | 1.00 |
| pr | 16bit_subcutaneous.cropped.jxl | 0 | 0/8192 | 1.00 |
| decoder | hopper.jxl | 0 | 0/49152 | 1.00 |
| decoder | hopper_gray.jxl | 0 | 0/16384 | 1.00 |
| decoder | transparent.jxl | 0 | 0/120000 | 1.00 |
| decoder | flower.jxl | 0 | 0/518400 | 1.10 |
| decoder | flower2.jxl | 0 | 0/202500 | 1.03 |
| decoder | 16bit_subcutaneous.cropped.jxl | 0 | 0/8192 | 0.99 |
| minsize | hopper.jxl | 0 | 0/49152 | 1.29 |
| minsize | hopper_gray.jxl | 0 | 0/16384 | 1.14 |
| minsize | transparent.jxl | 0 | 0/120000 | 1.07 |
| minsize | flower.jxl | 0 | 0/518400 | 1.38 |
| minsize | flower2.jxl | 0 | 0/202500 | 1.46 |
| minsize | 16bit_subcutaneous.cropped.jxl | 0 | 0/8192 | 1.03 |
| lto | hopper.jxl | 0 | 0/49152 | 1.28 |
| lto | hopper_gray.jxl | 0 | 0/16384 | 1.15 |
| lto | transparent.jxl | 0 | 0/120000 | 1.13 |
| lto | flower.jxl | 0 | 0/518400 | 1.42 |
| lto | flower2.jxl | 0 | 0/202500 | 1.49 |
| lto | 16bit_subcutaneous.cropped.jxl | 0 | 0/8192 | 1.10 |
| scalar | hopper.jxl | 1 | 736/49152 | 1.84 |
| scalar | hopper_gray.jxl | 1 | 218/16384 | 1.66 |
| scalar | transparent.jxl | 0 | 0/120000 | 1.11 |
| scalar | flower.jxl | 1 | 8139/518400 | 4.11 |
| scalar | flower2.jxl | 1 | 3032/202500 | 4.05 |
| scalar | 16bit_subcutaneous.cropped.jxl | 0 | 0/8192 | 1.07 |
