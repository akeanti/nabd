# Hardware

Hardware design files in this directory are licensed under the CERN Open Hardware Licence Version 2, Permissive ([LICENSE](LICENSE)).

Read the safety rules in [docs/hardware.md](../docs/hardware.md) before building a node. Nodes never connect directly to mains; voltage sensing goes only through an isolated 9 V AC-AC wall adapter, a resistor divider, and a midscale bias network.

| File | Contents | Status |
| --- | --- | --- |
| [BOM.csv](BOM.csv) | Bill of materials with example parts, indicative prices, and totals per tier | preliminary |
| KiCad 8 project | Shield for the ESP32-S3-DevKitC-1 supporting both tiers through jumpers | planned |
| Wiring diagrams | SVG wiring for breadboard and shield builds | planned |
| Assembly images | Photos for the workshop guide | planned |

Estimated cost from `BOM.csv`: 58.74 USD for tier A and 65.74 USD for tier B, at single-unit prices, without an enclosure.
