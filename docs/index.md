# Nabd

Nabd is an open network of low-cost GPS-synchronized ESP32 nodes that measure power grid frequency, rate of change of frequency (ROCOF), and voltage synchrophasors, with a collector server, a live map, and an open dataset. It is built for engineering students, makers, and power systems researchers.

!!! note "Status"
    Pre-release. The repository contains the build, test, and CI scaffold. Measurement firmware, collector, and map are under development.

![Live map screenshot placeholder](assets/live-map-placeholder.svg)

## Start here

- [Hardware and safety](hardware.md): the two hardware tiers, the isolated voltage front end, and the safety rules every node follows.
- [Privacy](privacy.md): how node locations are handled and what is published.
- [Architecture](architecture.md): how nodes, the collector, storage, the live map, and the dataset fit together.
- [Flash a node](flash.md): install firmware from the browser.

## Measurements

Each node reports frequency, ROCOF, and a single-phase voltage synchrophasor at 10, 25, or 50 frames per second, aligned to UTC second boundaries, together with quality flags for GPS lock, holdover, ADC clipping, and invalid data. Phasor estimation follows the P class of IEEE C37.118.1-2011 and its amendment C37.118.1a-2014, and the data stream follows IEEE C37.118.2-2011.
