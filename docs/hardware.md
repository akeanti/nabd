# Hardware and safety

## Safety

**Nodes never connect directly to mains.** Voltage sensing uses only three parts:

1. an isolated 9 V AC-AC wall adapter, which is a safety isolating transformer with an AC output,
2. a resistor divider, and
3. a midscale bias network.

The adapter's transformer is the isolation barrier between mains and the node. Everything on the node side, including the ESP32-S3 board, the GPS receiver, the USB supply, and any computer connected over USB, operates at extra-low voltage. Nothing in this project requires opening an adapter, an outlet, or a distribution board.

![Isolated voltage path of a node](assets/readme/signal-chain-light.svg#only-light)
![Isolated voltage path of a node](assets/readme/signal-chain-dark.svg#only-dark)

Rules for every node:

- Use a certified adapter marked as a safety isolating transformer (IEC 61558-2-6) or listed as a Class 2 transformer (UL 5085-3), with a 9 V AC output. The label shows the output as "9V AC" or "9V ~".
- DC adapters, switch-mode electronic transformers for halogen lamps, autotransformers, and variable transformers must not be used.
- Do not open or modify the adapter. Replace any adapter with a damaged case, cord, or plug.
- A higher-voltage adapter requires new divider values; see [Voltage front end](#voltage-front-end).
- Power the node over USB. Do not derive the node supply from the AC adapter: a rectifier draws current pulses that distort the waveform being measured.
- Contributions that add any direct mains connection, such as transformerless sensing, resistive droppers, or shunts, are not accepted.

## Hardware tiers

| | Tier A (workshop build) | Tier B (precision) |
| --- | --- | --- |
| Controller | ESP32-S3-DevKitC-1, 8 MB flash | same |
| GPS | NEO-6M or NEO-M8N with PPS output | same |
| ADC | ESP32-S3 internal 12-bit SAR ADC, ADC1, continuous DMA sampling | TI ADS131M02, 24-bit delta-sigma, 2 simultaneous channels, SPI |
| Sample timing | ADC clock derived from the ESP32-S3 crystal; sample blocks timestamped against the GPS-disciplined clock | each data-ready edge timestamped against the GPS-disciplined clock |
| Front end | isolated AC adapter, divider, midscale bias | same divider, routed to the ADS131M02 by jumpers on the shield |

One KiCad shield supports both tiers; jumpers select which ADC receives the divider output.

## Voltage front end

One adapter terminal connects to node ground. The other terminal drives a divider: R1 runs from the adapter terminal to the ADC input node, and R2 runs from the ADC input node to the bias node. Two equal resistors Rb hold the bias node at half of the 3.3 V supply, and Cb makes the bias node an AC ground. Ca is a small capacitor from the ADC input node to ground that supplies charge to the ADC sampling capacitor. A dual Schottky diode clamps the ADC input node to the supply rails.

```text
V_adc(t) = V_bias * R1 / (R1 + R2) + v_ac(t) * R2 / (R1 + R2)
```

The values below are preliminary until they are confirmed on the KiCad schematic and on hardware.

| Part | Value | Purpose |
| --- | --- | --- |
| R1 | 100 kΩ, 1 %, metal film | divider, top |
| R2 | 5.6 kΩ, 1 %, metal film | divider, bottom |
| Rb (2) | 10 kΩ, 1 % | bias divider from 3.3 V |
| Cb | 470 µF, 10 V, electrolytic, with 100 nF ceramic in parallel | bias decoupling |
| Ca | 1 nF, C0G | ADC input charge reservoir |
| D1 | BAT54S | clamp of the ADC input node to 3.3 V and ground |

Design numbers:

| Quantity | Value |
| --- | --- |
| Divider gain R2 / (R1 + R2) | 0.0530 |
| DC level at the ADC input node | 1.5625 V |
| Adapter output, nominal 9 V RMS | 12.7 V peak, ADC node 0.89 V to 2.24 V |
| Adapter output, worst case: unloaded output 30 % above nominal, mains 10 % high | 18.2 V peak, ADC node 0.60 V to 2.53 V |
| Design maximum | 20 V peak, ADC node 0.50 V to 2.62 V |
| ESP32-S3 ADC input range at 12 dB attenuation | about 0 V to 3.1 V; the margins avoid the nonlinear regions near both ends |
| Clamp current with a 24 V AC adapter connected by mistake (48.5 V peak worst case) | 0.45 mA, limited by R1 |
| Front-end phase shift, 45 Hz to 65 Hz | -0.16 degrees to -0.18 degrees |
| Phase shift spread for Cb tolerance of 20 % | 0.03 degrees |
| Bias network time constant | 2.4 s (corner at 0.07 Hz, which also filters supply noise on the bias) |

The fixed phase shift of the front end, and the larger and less predictable phase shift and ratio error of the AC adapter itself, are removed by per-adapter calibration of magnitude and phase. Absolute phase accuracy, and therefore TVE, depends on that calibration; frequency and ROCOF do not.

## GPS receiver

- The receiver must provide a pulse-per-second (PPS) output. NEO-M8N breakout boards usually expose PPS on a header pin. Many NEO-6M boards, such as the common GY-NEO6MV2, route PPS only to an LED, so a wire must be soldered to the module's time pulse pin.
- u-blox specifies the NEO-6M and NEO-M8N time pulse accuracy as 30 ns RMS with a clear sky view. One microsecond corresponds to 0.018 degrees at 50 Hz and 0.022 degrees at 60 Hz.
- Use an active antenna with a view of the sky. A window position usually works with reduced satellite count; the node reports holdover when the receiver loses its fix.

## Power

The node is powered over USB from a 5 V supply of at least 1 A. The AC adapter supplies only the divider current, below 0.2 mA, so its output waveform follows the mains waveform closely.
