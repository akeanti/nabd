# Firmware

PlatformIO project for the ESP32-S3 node, built on ESP-IDF.

| Environment | Purpose |
| --- | --- |
| `tier_a` | Firmware for the ESP32-S3 internal ADC front end |
| `tier_b` | Firmware for the ADS131M02 front end |
| `native` | Host unit tests with Unity |

```bash
pip install -r requirements.txt
pio test -e native
pio run -e tier_a
pio run -e tier_a -t upload
pio device monitor
```

| Path | Contents |
| --- | --- |
| `lib/nabd_dsp` | Phasor, frequency, and ROCOF estimation. Pure C++17, host-testable. |
| `lib/nabd_time` | GPS PPS clock discipline with an injected time source, host-testable. |
| `lib/nabd_hal` | `AdcSource` interface, ESP32-S3 internal ADC and ADS131M02 backends, PPS capture, NMEA parser. |
| `lib/nabd_c37118` | IEEE C37.118.2 frame encoding. Pure C++17, host-testable. |
| `src` | Tasks, networking, provisioning, and `app_main`. |
| `test` | Unity tests run by `pio test -e native`. |
| `partitions.csv` | Flash layout for 8 MB: NVS, two OTA application slots, core dump. |
| `sdkconfig.defaults` | ESP-IDF configuration shared by both tiers. |

The firmware version reported at boot comes from `git describe` at build time.
