# Flash a node

Connect the ESP32-S3-DevKitC-1 to this computer with a USB data cable and press the button for your hardware tier. Flashing uses the Web Serial API, which is available in Chrome, Edge, and Opera on desktop operating systems.

<script type="module" src="https://unpkg.com/esp-web-tools@10.4.0/dist/web/install-button.js?module"></script>

| Hardware | Install |
| --- | --- |
| Tier A, internal ADC | <esp-web-install-button manifest="firmware/manifest-tier-a.json"><span slot="unsupported">This browser does not support Web Serial. Use Chrome or Edge on a desktop computer.</span></esp-web-install-button> |
| Tier B, ADS131M02 | <esp-web-install-button manifest="firmware/manifest-tier-b.json"><span slot="unsupported">This browser does not support Web Serial. Use Chrome or Edge on a desktop computer.</span></esp-web-install-button> |

The firmware on this page is the latest GitHub release. Until the first release is published, the buttons report that no firmware is available.

If the board is not detected, hold the BOOT button while pressing RESET, then release BOOT and try again. On Windows, a board connected through its UART port may need the driver for its USB to UART bridge chip.
