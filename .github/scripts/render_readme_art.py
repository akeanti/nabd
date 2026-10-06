import argparse
import math
import sys
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from pathlib import Path
from xml.sax.saxutils import escape

ASSET_DIR = Path(__file__).resolve().parents[2] / "docs" / "assets" / "readme"
SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace"
AVERAGE_GLYPH_WIDTH = 0.56

Point = tuple[float, float]


@dataclass(frozen=True)
class Palette:
    name: str
    canvas: str
    canvas_tint: str
    panel: str
    border: str
    text: str
    muted: str
    grid: str
    brand: str
    brand_soft: str
    on_brand: str
    amber: str
    gold: str
    violet: str
    blue: str
    green: str
    green_soft: str
    red: str
    red_soft: str
    water: str
    land: str
    land_border: str


LIGHT = Palette(
    name="light",
    canvas="#F6F8FA",
    canvas_tint="#E4F3F4",
    panel="#FFFFFF",
    border="#D0D7DE",
    text="#1F2328",
    muted="#59636E",
    grid="#E3E8ED",
    brand="#0A7E8C",
    brand_soft="#D7EFF1",
    on_brand="#FFFFFF",
    amber="#B35900",
    gold="#BF8700",
    violet="#6E40C9",
    blue="#0969DA",
    green="#1A7F37",
    green_soft="#E6F6EA",
    red="#CF222E",
    red_soft="#FFEBE9",
    water="#E9F1F7",
    land="#FBFCFD",
    land_border="#C5D1DC",
)

DARK = Palette(
    name="dark",
    canvas="#0D1117",
    canvas_tint="#0B2327",
    panel="#161B22",
    border="#30363D",
    text="#E6EDF3",
    muted="#9198A1",
    grid="#21282F",
    brand="#3CC5D3",
    brand_soft="#103137",
    on_brand="#06181B",
    amber="#F0A030",
    gold="#D29922",
    violet="#A97BFF",
    blue="#4493F8",
    green="#3FB950",
    green_soft="#11261A",
    red="#F85149",
    red_soft="#3A1618",
    water="#0E1822",
    land="#19212B",
    land_border="#2F3B48",
)


def number(value: float) -> str:
    text = f"{value:.1f}".removesuffix(".0")
    return "0" if text == "-0" else text


def text_width(content: str, size: float) -> float:
    return len(content) * size * AVERAGE_GLYPH_WIDTH


def label(
    x: float,
    y: float,
    content: str,
    *,
    size: float,
    fill: str,
    weight: int = 400,
    family: str = SANS,
    anchor: str = "start",
    attributes: str = "",
) -> str:
    return (
        f'<text x="{number(x)}" y="{number(y)}" font-family="{family}" font-size="{number(size)}" '
        f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}"{attributes}>'
        f"{escape(content)}</text>"
    )


def document(
    width: int, height: int, title: str, description: str, body: Sequence[str], css: str = ""
) -> str:
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
        f'<title id="title">{escape(title)}</title>',
        f'<desc id="desc">{escape(description)}</desc>',
    ]
    if css:
        lines.append(f"<style>{css}</style>")
    lines.extend(body)
    lines.append("</svg>")
    return "\n".join(lines) + "\n"


def polyline_path(points: Sequence[Point]) -> str:
    head, *tail = points
    return f"M{number(head[0])} {number(head[1])} L" + " ".join(
        f"{number(x)} {number(y)}" for x, y in tail
    )


def wave_path(
    x_start: float,
    x_end: float,
    center_y: float,
    amplitude: float,
    wavelength: float,
    *,
    phase: float = 0.0,
    shape: Callable[[float], float] = math.sin,
    step: float = 2.0,
) -> str:
    count = max(1, round((x_end - x_start) / step))
    points = []
    for index in range(count + 1):
        x = x_start + index * (x_end - x_start) / count
        angle = 2 * math.pi * (x - x_start) / wavelength + phase
        points.append((x, center_y - amplitude * shape(angle)))
    return polyline_path(points)


def smooth_closed_path(points: Sequence[Point]) -> str:
    count = len(points)
    commands = [f"M{number(points[0][0])} {number(points[0][1])}"]
    for index in range(count):
        before = points[index - 1]
        start = points[index]
        end = points[(index + 1) % count]
        after = points[(index + 2) % count]
        control_1 = (start[0] + (end[0] - before[0]) / 6, start[1] + (end[1] - before[1]) / 6)
        control_2 = (end[0] - (after[0] - start[0]) / 6, end[1] - (after[1] - start[1]) / 6)
        commands.append(
            f"C{number(control_1[0])} {number(control_1[1])} {number(control_2[0])} "
            f"{number(control_2[1])} {number(end[0])} {number(end[1])}"
        )
    return " ".join(commands) + " Z"


def mix(color_a: str, color_b: str, fraction: float) -> str:
    channels_a = [int(color_a[i : i + 2], 16) for i in (1, 3, 5)]
    channels_b = [int(color_b[i : i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(
        f"{round(a + (b - a) * fraction):02X}" for a, b in zip(channels_a, channels_b, strict=True)
    )


def grid_lines(x: float, y: float, width: float, height: float, spacing: float, color: str) -> str:
    lines = [
        f'<line x1="{number(x + offset)}" y1="{number(y)}" x2="{number(x + offset)}" '
        f'y2="{number(y + height)}"/>'
        for offset in _steps(spacing, width)
    ]
    lines += [
        f'<line x1="{number(x)}" y1="{number(y + offset)}" x2="{number(x + width)}" '
        f'y2="{number(y + offset)}"/>'
        for offset in _steps(spacing, height)
    ]
    return f'<g stroke="{color}" stroke-width="1">' + "".join(lines) + "</g>"


def _steps(spacing: float, extent: float) -> list[float]:
    return [spacing * index for index in range(1, math.ceil(extent / spacing))]


def pill(x: float, y: float, content: str, *, fill: str, stroke: str, color: str) -> str:
    size = 14.0
    width = text_width(content, size) + 28
    return (
        f'<rect x="{number(x)}" y="{number(y)}" width="{number(width)}" height="30" rx="15" '
        f'fill="{fill}" stroke="{stroke}"/>'
        + label(x + width / 2, y + 20, content, size=size, fill=color, weight=600, anchor="middle")
    )


MOTION_CSS = (
    ".turn{transform-box:fill-box;transform-origin:center}"
    ".ring{transform-box:fill-box;transform-origin:center;opacity:.3}"
    "@media (prefers-reduced-motion:no-preference){"
    ".turn-fast{animation:turn 4s linear infinite}"
    ".turn-slow{animation:turn 12s linear infinite}"
    ".flow-right{animation:flow-right 4s linear infinite}"
    ".flow-left{animation:flow-left 12s linear infinite}"
    ".ring{animation:pulse 3s ease-out infinite}"
    ".dash{animation:dash 1.2s linear infinite}"
    "}"
    "@keyframes turn{to{transform:rotate(-360deg)}}"
    "@keyframes flow-right{to{transform:translateX(160px)}}"
    "@keyframes flow-left{to{transform:translateX(-152px)}}"
    "@keyframes pulse{0%{transform:scale(1);opacity:.55}100%{transform:scale(3.4);opacity:0}}"
    "@keyframes dash{to{stroke-dashoffset:-20}}"
)


def hero(p: Palette) -> str:
    width, height = 1280, 360
    screen_x, screen_y, screen_w, screen_h = 676, 36, 568, 288
    pivot_x, pivot_y, radius = 790, 188, 82
    wave_start, wave_end, wavelength = 900, 1220, 160
    chips = ["IEEE C37.118", "ESP32-S3", "GPS PPS", "Open hardware", "Open data"]
    trace = wave_path(wave_start - wavelength, wave_end, pivot_y, radius, wavelength, phase=math.pi)
    body = [
        "<defs>",
        '<linearGradient id="hero-bg" x1="0" y1="0" x2="1" y2="0">',
        f'<stop offset="0" stop-color="{p.canvas}"/>',
        f'<stop offset="1" stop-color="{p.canvas_tint}"/>',
        "</linearGradient>",
        f'<clipPath id="hero-screen"><rect x="{screen_x}" y="{screen_y}" width="{screen_w}" '
        f'height="{screen_h}" rx="18"/></clipPath>',
        f'<clipPath id="hero-trace"><rect x="{wave_start}" y="{screen_y}" '
        f'width="{wave_end - wave_start}" height="{screen_h}"/></clipPath>',
        "</defs>",
        f'<rect width="{width}" height="{height}" rx="24" fill="url(#hero-bg)"/>',
        f'<rect x=".5" y=".5" width="{width - 1}" height="{height - 1}" rx="24" fill="none" '
        f'stroke="{p.border}"/>',
        label(
            64,
            104,
            "OPEN GRID MEASUREMENT NETWORK",
            size=15,
            fill=p.brand,
            weight=700,
            attributes=' letter-spacing="3"',
        ),
        label(
            60, 196, "Nabd", size=104, fill=p.text, weight=800, attributes=' letter-spacing="-3"'
        ),
        label(64, 244, "GPS-synchronized frequency, ROCOF, and", size=24, fill=p.muted),
        label(64, 276, "synchrophasor measurement on ESP32-S3 nodes", size=24, fill=p.muted),
    ]
    chip_x = 64.0
    for chip in chips:
        body.append(pill(chip_x, 298, chip, fill=p.panel, stroke=p.border, color=p.text))
        chip_x += text_width(chip, 14) + 28 + 10
    body += [
        f'<rect x="{screen_x}" y="{screen_y}" width="{screen_w}" height="{screen_h}" rx="18" '
        f'fill="{p.panel}" stroke="{p.border}"/>',
        '<g clip-path="url(#hero-screen)">',
        grid_lines(screen_x, screen_y, screen_w, screen_h, 32, p.grid),
        "</g>",
        f'<circle cx="{screen_x + 26}" cy="{screen_y + 24}" r="5" fill="{p.red}"/>',
        f'<circle cx="{screen_x + 44}" cy="{screen_y + 24}" r="5" fill="{p.amber}"/>',
        f'<circle cx="{screen_x + 62}" cy="{screen_y + 24}" r="5" fill="{p.green}"/>',
        label(
            screen_x + 80,
            screen_y + 29,
            "node 07  |  GPS locked  |  50 Hz nominal",
            size=13,
            fill=p.muted,
            family=MONO,
        ),
        f'<circle cx="{pivot_x}" cy="{pivot_y}" r="{radius}" fill="none" stroke="{p.border}" '
        f'stroke-width="1.5" stroke-dasharray="4 5"/>',
        f'<line x1="{pivot_x - radius - 12}" y1="{pivot_y}" x2="{wave_end}" y2="{pivot_y}" '
        f'stroke="{p.border}" stroke-width="1.5"/>',
        f'<line x1="{pivot_x}" y1="{pivot_y - radius - 12}" x2="{pivot_x}" '
        f'y2="{pivot_y + radius + 12}" stroke="{p.border}" stroke-width="1.5"/>',
        '<g clip-path="url(#hero-trace)"><g class="flow-right">',
        f'<path d="{trace}" fill="none" stroke="{p.brand}" stroke-width="3.5" '
        'stroke-linecap="round" stroke-linejoin="round"/>',
        "</g></g>",
        f'<g transform="translate({pivot_x} {pivot_y})"><g class="turn turn-fast">',
        f'<circle r="{radius}" fill="none"/>',
        f'<line x1="0" y1="0" x2="{radius}" y2="0" stroke="{p.amber}" stroke-width="4" '
        'stroke-linecap="round"/>',
        f'<circle cx="{radius}" cy="0" r="6.5" fill="{p.amber}"/>',
        "</g></g>",
        f'<circle cx="{pivot_x}" cy="{pivot_y}" r="5" fill="{p.text}"/>',
        label(
            pivot_x,
            screen_y + screen_h - 18,
            "phasor V and angle",
            size=13,
            fill=p.muted,
            family=MONO,
            anchor="middle",
        ),
        label(
            wave_start + 12,
            screen_y + screen_h - 18,
            "v(t) at the outlet, UTC-aligned",
            size=13,
            fill=p.muted,
            family=MONO,
        ),
    ]
    return document(
        width,
        height,
        "Nabd: GPS-synchronized grid measurement on ESP32-S3",
        "Project banner with a rotating voltage phasor that draws the outlet waveform in time.",
        body,
        MOTION_CSS,
    )


LANDMASSES = (
    "96,236 132,196 188,182 226,150 286,146 334,166 390,160 438,190 470,236 456,282 474,318 "
    "430,350 372,344 330,384 268,378 222,350 170,356 122,318 106,276",
    "548,170 590,132 648,140 700,112 760,128 806,160 842,214 828,262 790,286 772,330 716,338 "
    "668,312 612,322 570,284 560,232",
    "336,456 386,424 446,436 500,408 560,420 624,436 676,474 706,524 672,560 612,574 552,560 "
    "492,580 430,566 378,536 342,500",
    "748,440 786,418 830,428 852,462 836,500 800,512 764,496 744,470",
)


def parse_points(spec: str) -> list[Point]:
    return [(float(x), float(y)) for x, y in (pair.split(",") for pair in spec.split())]


def deviation_stops(p: Palette) -> tuple[str, str, str, str, str]:
    return (p.blue, mix(p.blue, p.green, 0.5), p.green, p.gold, p.amber)


def deviation_color(p: Palette, millihertz: float, full_scale: float) -> str:
    stops = deviation_stops(p)
    position = (max(-1.0, min(1.0, millihertz / full_scale)) + 1) * 2
    index = min(3, int(position))
    return mix(stops[index], stops[index + 1], position - index)


def map_traces(seed: float, amplitude: float, count: int) -> list[float]:
    return [
        amplitude
        * (
            0.62 * math.sin(2 * math.pi * index / 46 + seed)
            + 0.28 * math.sin(2 * math.pi * index / 13 + 2.1 * seed)
            + 0.10 * math.sin(2 * math.pi * index / 5 + 3.7 * seed)
        )
        for index in range(count)
    ]


def chart_path(values: Sequence[float], x: float, width: float, center_y: float) -> str:
    step = width / (len(values) - 1)
    return polyline_path(
        [(x + index * step, center_y - value) for index, value in enumerate(values)]
    )


def live_map(p: Palette) -> str:
    width, height = 1280, 620
    map_x, map_y, map_w, map_h = 32, 76, 836, 512
    side_x = 888
    nodes = [
        (205, 252, 8.0),
        (300, 228, 0.0),
        (385, 292, 5.0),
        (652, 188, -4.0),
        (760, 232, -7.0),
        (700, 286, 2.0),
        (450, 482, 15.0),
        (560, 500, 12.0),
        (618, 458, 9.0),
        (805, 466, -14.0),
    ]
    reference_index = 1
    body = [
        "<defs>",
        f'<clipPath id="map-area"><rect x="{map_x}" y="{map_y}" width="{map_w}" '
        f'height="{map_h}" rx="12"/></clipPath>',
        '<linearGradient id="legend" x1="0" y1="0" x2="1" y2="0">',
        *(
            f'<stop offset="{number(index / 4)}" stop-color="{color}"/>'
            for index, color in enumerate(deviation_stops(p))
        ),
        "</linearGradient>",
        "</defs>",
        f'<rect x=".5" y=".5" width="{width - 1}" height="{height - 1}" rx="20" fill="{p.canvas}" '
        f'stroke="{p.border}"/>',
        f'<circle cx="34" cy="38" r="6" fill="{p.red}"/>',
        f'<circle cx="54" cy="38" r="6" fill="{p.amber}"/>',
        f'<circle cx="74" cy="38" r="6" fill="{p.green}"/>',
        label(100, 44, "Nabd live map", size=17, fill=p.text, weight=700),
        label(
            226,
            44,
            "10 nodes  |  reference node 2  |  50 frames/s",
            size=13,
            fill=p.muted,
            family=MONO,
        ),
        f'<rect x="{width - 168}" y="22" width="136" height="32" rx="16" fill="{p.amber}"/>',
        label(
            width - 100,
            43,
            "ILLUSTRATION",
            size=13,
            fill=p.on_brand,
            weight=800,
            anchor="middle",
            attributes=' letter-spacing="1.5"',
        ),
        f'<rect x="{map_x}" y="{map_y}" width="{map_w}" height="{map_h}" rx="12" '
        f'fill="{p.water}" stroke="{p.border}"/>',
        '<g clip-path="url(#map-area)">',
        grid_lines(map_x, map_y, map_w, map_h, 64, p.grid),
    ]
    body += [
        f'<path d="{smooth_closed_path(points)}" fill="{p.land}" stroke="{p.land_border}" '
        'stroke-width="1.5"/>'
        for points in map(parse_points, LANDMASSES)
    ]
    reference_x, reference_y, _ = nodes[reference_index]
    body += [
        f'<line x1="{reference_x}" y1="{reference_y}" x2="{x}" y2="{y}" stroke="{p.brand}" '
        'stroke-width="1" stroke-dasharray="3 5" opacity=".55"/>'
        for index, (x, y, _) in enumerate(nodes)
        if index != reference_index
    ]
    for index, (x, y, millihertz) in enumerate(nodes):
        color = deviation_color(p, millihertz, full_scale=15)
        delay = number(-0.31 * index)
        body.append(
            f'<circle class="ring" cx="{x}" cy="{y}" r="8" fill="none" stroke="{color}" '
            f'stroke-width="2" style="animation-delay:{delay}s"/>'
        )
        body.append(
            f'<circle cx="{x}" cy="{y}" r="8" fill="{color}" stroke="{p.panel}" '
            'stroke-width="2.5"/>'
        )
    body += [
        f'<circle cx="{reference_x}" cy="{reference_y}" r="15" fill="none" stroke="{p.text}" '
        'stroke-width="2"/>',
        label(reference_x + 20, reference_y - 14, "reference", size=13, fill=p.text, weight=600),
        "</g>",
        f'<rect x="{map_x + 16}" y="{map_y + map_h - 72}" width="372" height="56" rx="10" '
        f'fill="{p.panel}" stroke="{p.border}" opacity=".96"/>',
        label(
            map_x + 32, map_y + map_h - 48, "Frequency deviation", size=13, fill=p.text, weight=600
        ),
        f'<rect x="{map_x + 172}" y="{map_y + map_h - 58}" width="200" height="10" rx="5" '
        'fill="url(#legend)"/>',
        label(map_x + 172, map_y + map_h - 26, "-15 mHz", size=12, fill=p.muted, family=MONO),
        label(
            map_x + 272,
            map_y + map_h - 26,
            "0",
            size=12,
            fill=p.muted,
            family=MONO,
            anchor="middle",
        ),
        label(
            map_x + 372,
            map_y + map_h - 26,
            "+15 mHz",
            size=12,
            fill=p.muted,
            family=MONO,
            anchor="end",
        ),
    ]
    panels = [
        (76, 168, "Frequency, 60 s window"),
        (256, 132, "Angle relative to the reference"),
        (400, 188, "Events"),
    ]
    for top, panel_height, title in panels:
        body.append(
            f'<rect x="{side_x}" y="{top}" width="{width - side_x - 32}" height="{panel_height}" '
            f'rx="12" fill="{p.panel}" stroke="{p.border}"/>'
        )
        body.append(label(side_x + 18, top + 28, title, size=14, fill=p.text, weight=600))
    chart_x, chart_w = side_x + 18, width - side_x - 32 - 36
    body += [
        f'<line x1="{chart_x}" y1="170" x2="{chart_x + chart_w}" y2="170" stroke="{p.border}" '
        'stroke-dasharray="4 4"/>',
        label(
            chart_x + chart_w,
            104,
            "nominal 50.000 Hz",
            size=12,
            fill=p.muted,
            family=MONO,
            anchor="end",
        ),
    ]
    for seed, color in ((0.3, p.brand), (1.7, p.violet), (3.1, p.amber)):
        body.append(
            f'<path d="{chart_path(map_traces(seed, 30, 90), chart_x, chart_w, 170)}" fill="none" '
            f'stroke="{color}" stroke-width="2" stroke-linejoin="round"/>'
        )
    angle_values = [
        34 * math.exp(-index / 55) * math.sin(2 * math.pi * index / 21) for index in range(90)
    ]
    body += [
        f'<line x1="{chart_x}" y1="326" x2="{chart_x + chart_w}" y2="326" stroke="{p.border}" '
        'stroke-dasharray="4 4"/>',
        f'<path d="{chart_path(angle_values, chart_x, chart_w, 326)}" fill="none" '
        f'stroke="{p.violet}" stroke-width="2" stroke-linejoin="round"/>',
        f'<path d="{chart_path([-0.6 * v for v in angle_values], chart_x, chart_w, 326)}" '
        f'fill="none" stroke="{p.brand}" stroke-width="2" stroke-linejoin="round"/>',
    ]
    events = [
        (p.amber, "Frequency excursion", "14:02:11"),
        (p.red, "ROCOF spike", "14:02:12"),
        (p.violet, "Angle oscillation, 0.31 Hz", "14:02:19"),
        (p.green, "All nodes GPS locked", "14:03:00"),
    ]
    for row, (color, event, time) in enumerate(events):
        y = 452 + row * 34
        body.append(f'<circle cx="{side_x + 24}" cy="{y - 5}" r="5" fill="{color}"/>')
        body.append(label(side_x + 38, y, event, size=13, fill=p.text))
        body.append(label(width - 50, y, time, size=12, fill=p.muted, family=MONO, anchor="end"))
    body.append(
        label(
            width / 2,
            height - 12,
            "Illustration of the planned live map. Node positions are " "rounded to city level.",
            size=13,
            fill=p.muted,
            anchor="middle",
        )
    )
    return document(
        width,
        height,
        "Illustration of the planned Nabd live map",
        "Mock-up of the planned live map: nodes colored by frequency deviation around a reference "
        "node, frequency and relative angle charts, and an event list. Values are illustrative.",
        body,
        MOTION_CSS,
    )


def synchrophasor(p: Palette) -> str:
    width, height = 1280, 420
    pivot_x, pivot_y, radius = 230, 196, 118
    chart_start, chart_end, wavelength, amplitude = 470, 1230, 152, 92
    lead_degrees = 35
    reference = wave_path(chart_start, chart_end, pivot_y, amplitude, wavelength, shape=math.cos)
    measured = wave_path(
        chart_start,
        chart_end + wavelength,
        pivot_y,
        amplitude,
        wavelength,
        phase=math.radians(lead_degrees),
        shape=math.cos,
    )
    body = [
        "<defs>",
        f'<clipPath id="chart"><rect x="{chart_start}" y="60" width="{chart_end - chart_start}" '
        'height="280"/></clipPath>',
        "</defs>",
        f'<rect x=".5" y=".5" width="{width - 1}" height="{height - 1}" rx="20" fill="{p.canvas}" '
        f'stroke="{p.border}"/>',
        label(40, 46, "How a node reports a synchrophasor", size=18, fill=p.text, weight=700),
        f'<circle cx="{pivot_x}" cy="{pivot_y}" r="{radius}" fill="{p.panel}" stroke="{p.border}" '
        'stroke-width="1.5"/>',
        f'<line x1="{pivot_x - radius}" y1="{pivot_y}" x2="{pivot_x + radius}" y2="{pivot_y}" '
        f'stroke="{p.grid}" stroke-width="1.5"/>',
        f'<line x1="{pivot_x}" y1="{pivot_y - radius}" x2="{pivot_x}" y2="{pivot_y + radius}" '
        f'stroke="{p.grid}" stroke-width="1.5"/>',
        f'<line x1="{pivot_x}" y1="{pivot_y}" x2="{pivot_x + radius}" y2="{pivot_y}" '
        f'stroke="{p.muted}" stroke-width="3" stroke-dasharray="7 6"/>',
        label(
            pivot_x + radius - 4,
            pivot_y + 24,
            "UTC reference",
            size=13,
            fill=p.muted,
            family=MONO,
            anchor="end",
        ),
        f'<g transform="translate({pivot_x} {pivot_y}) rotate(-{lead_degrees})">',
        '<g class="turn turn-slow">',
        f'<circle r="{radius}" fill="none"/>',
        f'<line x1="0" y1="0" x2="{radius - 8}" y2="0" stroke="{p.brand}" stroke-width="5" '
        'stroke-linecap="round"/>',
        f'<path d="M{radius} 0 L{radius - 18} -9 L{radius - 18} 9 Z" fill="{p.brand}"/>',
        "</g></g>",
        f'<circle cx="{pivot_x}" cy="{pivot_y}" r="6" fill="{p.text}"/>',
        label(
            pivot_x,
            pivot_y + radius + 30,
            "phasor: magnitude and angle",
            size=13,
            fill=p.muted,
            family=MONO,
            anchor="middle",
        ),
    ]
    for index in range(6):
        x = chart_start + index * wavelength
        caption = "UTC second" if index == 0 else f"+{20 * index} ms"
        body.append(
            f'<line x1="{x}" y1="76" x2="{x}" y2="316" stroke="{p.border}" stroke-width="1.5" '
            'stroke-dasharray="3 5"/>'
        )
        body.append(label(x, 338, caption, size=12, fill=p.muted, family=MONO, anchor="middle"))
    body += [
        f'<line x1="{chart_start}" y1="{pivot_y}" x2="{chart_end}" y2="{pivot_y}" '
        f'stroke="{p.grid}" stroke-width="1.5"/>',
        f'<path d="{reference}" fill="none" stroke="{p.muted}" stroke-width="2.5" '
        'stroke-dasharray="8 7"/>',
        '<g clip-path="url(#chart)"><g class="flow-left">',
        f'<path d="{measured}" fill="none" stroke="{p.brand}" stroke-width="3.5" '
        'stroke-linejoin="round"/>',
        "</g></g>",
        f'<line x1="{chart_start}" y1="60" x2="{chart_start + 28}" y2="60" stroke="{p.brand}" '
        'stroke-width="3.5"/>',
        label(chart_start + 38, 65, "measured voltage", size=13, fill=p.text),
        f'<line x1="{chart_start + 190}" y1="60" x2="{chart_start + 218}" y2="60" '
        f'stroke="{p.muted}" stroke-width="2.5" stroke-dasharray="8 7"/>',
        label(chart_start + 228, 65, "50 Hz cosine locked to UTC", size=13, fill=p.text),
        label(
            40,
            382,
            "Above 50 Hz the measured wave runs ahead of the UTC reference, so the "
            "phasor turns. Its angle is the synchrophasor;",
            size=14,
            fill=p.muted,
        ),
        label(
            40,
            404,
            "the rate of turning gives frequency, and the change of that rate gives "
            "ROCOF. Rotation is slowed here for display.",
            size=14,
            fill=p.muted,
        ),
    ]
    return document(
        width,
        height,
        "How a node reports a synchrophasor",
        "A voltage phasor turns against a 50 Hz cosine reference locked to UTC, while the measured "
        "waveform drifts ahead of the reference at reporting instants spaced 20 ms apart.",
        body,
        MOTION_CSS,
    )


def transformer_symbol(center_x: float, top: float, winding: str, core: str) -> str:
    height = 36
    primary = f"M{number(center_x - 11)} {number(top)}" + " a6 6 0 0 1 0 12" * 3
    secondary = f"M{number(center_x + 11)} {number(top)}" + " a6 6 0 0 0 0 12" * 3
    core_lines = "".join(
        f'<line x1="{number(center_x + offset)}" y1="{number(top - 4)}" '
        f'x2="{number(center_x + offset)}" y2="{number(top + height + 4)}"/>'
        for offset in (-2.5, 2.5)
    )
    return (
        f'<g fill="none" stroke="{winding}" stroke-width="2.5">'
        f'<path d="{primary}"/><path d="{secondary}"/></g>'
        f'<g stroke="{core}" stroke-width="2.5">{core_lines}</g>'
    )


def signal_chain(p: Palette) -> str:
    width, height = 1280, 320
    block_y, block_w, block_h, gap, first_x = 100, 168, 112, 40, 40
    barrier_x = first_x + block_w + gap + block_w / 2
    middle_y = block_y + block_h / 2
    blocks = [
        ("Wall outlet", "230 V or 120 V AC", "never wired to the node"),
        ("AC-AC adapter", "", ""),
        ("Divider", "100 kΩ and 5.6 kΩ", "gain 0.053"),
        ("Midscale bias", "1.65 V reference", "470 µF to ground"),
        ("ADC", "ESP32-S3 12-bit", "or ADS131M02 24-bit"),
        ("DSP and GPS time", "phasor, frequency,", "ROCOF, UTC tags"),
    ]
    body = [
        f'<rect x=".5" y=".5" width="{width - 1}" height="{height - 1}" rx="20" fill="{p.canvas}" '
        f'stroke="{p.border}"/>',
        f'<rect x="16" y="16" width="{number(barrier_x - 16)}" height="{height - 32}" rx="14" '
        f'fill="{p.red_soft}"/>',
        f'<rect x="{number(barrier_x)}" y="16" width="{number(width - 16 - barrier_x)}" '
        f'height="{height - 32}" rx="14" fill="{p.green_soft}"/>',
        label(
            36,
            52,
            "MAINS SIDE",
            size=13,
            fill=p.red,
            weight=800,
            attributes=' letter-spacing="1.5"',
        ),
        label(36, 74, "hazardous voltage, sealed in the adapter", size=13, fill=p.text),
        label(
            barrier_x + 24,
            52,
            "NODE SIDE",
            size=13,
            fill=p.green,
            weight=800,
            attributes=' letter-spacing="1.5"',
        ),
        label(barrier_x + 24, 74, "extra-low voltage only; powered over USB", size=13, fill=p.text),
    ]
    for index, (title, line_1, line_2) in enumerate(blocks):
        x = first_x + index * (block_w + gap)
        center_x = x + block_w / 2
        body.append(
            f'<rect x="{x}" y="{block_y}" width="{block_w}" height="{block_h}" rx="12" '
            f'fill="{p.panel}" stroke="{p.border}" stroke-width="1.5"/>'
        )
        if line_1:
            body += [
                label(
                    center_x, block_y + 36, title, size=16, fill=p.text, weight=700, anchor="middle"
                ),
                label(center_x, block_y + 62, line_1, size=13, fill=p.muted, anchor="middle"),
                label(center_x, block_y + 84, line_2, size=13, fill=p.muted, anchor="middle"),
            ]
        else:
            body += [
                label(
                    center_x, block_y + 28, title, size=16, fill=p.text, weight=700, anchor="middle"
                ),
                transformer_symbol(center_x, block_y + 40, winding=p.text, core=p.red),
                label(
                    center_x,
                    block_y + 100,
                    "certified, 9 V AC out",
                    size=13,
                    fill=p.muted,
                    anchor="middle",
                ),
            ]
        if index < len(blocks) - 1:
            start_x = x + block_w + 4
            end_x = x + block_w + gap - 4
            body += [
                f'<line class="dash" x1="{start_x}" y1="{number(middle_y)}" x2="{end_x - 8}" '
                f'y2="{number(middle_y)}" stroke="{p.brand}" stroke-width="3" '
                'stroke-dasharray="6 4"/>',
                f'<path d="M{end_x} {number(middle_y)} L{end_x - 10} {number(middle_y - 6)} '
                f'L{end_x - 10} {number(middle_y + 6)} Z" fill="{p.brand}"/>',
            ]
    barrier_segments = ((28, block_y - 6), (block_y + block_h + 6, 250))
    body += [
        f'<line x1="{number(barrier_x)}" y1="{top}" x2="{number(barrier_x)}" y2="{bottom}" '
        f'stroke="{p.red}" stroke-width="3" stroke-dasharray="8 6"/>'
        for top, bottom in barrier_segments
    ]
    body += [
        label(
            barrier_x, 270, "isolation barrier", size=13, fill=p.red, weight=700, anchor="middle"
        ),
        label(
            first_x + 2 * (block_w + gap) - gap / 2,
            240,
            "at most 20 V peak",
            size=13,
            fill=p.text,
            family=MONO,
            anchor="middle",
        ),
        label(
            first_x + 4 * (block_w + gap) - gap / 2,
            240,
            "0.50 V to 2.62 V",
            size=13,
            fill=p.text,
            family=MONO,
            anchor="middle",
        ),
        label(
            width / 2,
            300,
            "The only path to the grid is the transformer inside a certified "
            "adapter. The adapter carries only the divider current, below 0.2 mA.",
            size=13,
            fill=p.muted,
            anchor="middle",
        ),
    ]
    return document(
        width,
        height,
        "Isolated voltage path of a Nabd node",
        "Signal chain from the wall outlet through a certified isolating AC-AC adapter, a resistor "
        "divider, a midscale bias, and the ADC to the DSP. The adapter's transformer is the "
        "isolation barrier between the mains side and the extra-low voltage node side.",
        body,
        MOTION_CSS,
    )


def flash_button(p: Palette) -> str:
    width, height = 480, 88
    chip_x, chip_y = 30, 26
    pins = "".join(
        f'<line x1="{chip_x + offset}" y1="{chip_y - 6}" x2="{chip_x + offset}" y2="{chip_y}"/>'
        f'<line x1="{chip_x + offset}" y1="{chip_y + 36}" x2="{chip_x + offset}" '
        f'y2="{chip_y + 42}"/>'
        for offset in (9, 18, 27)
    )
    body = [
        f'<rect x="4" y="4" width="{width - 8}" height="{height - 8}" rx="18" fill="{p.brand}"/>',
        f'<g stroke="{p.on_brand}" stroke-width="2.5" stroke-linecap="round" fill="none">',
        f'<rect x="{chip_x}" y="{chip_y}" width="36" height="36" rx="6"/>',
        f'<rect x="{chip_x + 10}" y="{chip_y + 10}" width="16" height="16" rx="2"/>',
        pins,
        "</g>",
        label(88, 44, "Flash a node from your browser", size=21, fill=p.on_brand, weight=700),
        label(
            88,
            66,
            "ESP Web Tools in Chrome or Edge; no toolchain needed",
            size=13,
            fill=p.on_brand,
            attributes=' opacity=".88"',
        ),
    ]
    return document(
        width,
        height,
        "Flash a node from your browser",
        "Button linking to the browser-based firmware installer.",
        body,
    )


ARTWORK: dict[str, Callable[[Palette], str]] = {
    "hero": hero,
    "live-map": live_map,
    "synchrophasor": synchrophasor,
    "signal-chain": signal_chain,
    "flash-button": flash_button,
}


def rendered_files() -> dict[Path, str]:
    return {
        ASSET_DIR / f"{name}-{palette.name}.svg": render(palette)
        for name, render in ARTWORK.items()
        for palette in (LIGHT, DARK)
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render the README and documentation artwork in docs/assets/readme."
    )
    parser.add_argument(
        "--check", action="store_true", help="fail if a committed file differs from the output"
    )
    check = parser.parse_args().check
    stale = []
    for path, content in rendered_files().items():
        if check:
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                stale.append(path)
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8", newline="\n")
    for path in stale:
        print(f"{path.relative_to(ASSET_DIR.parents[2])}: out of date; run {Path(__file__).name}")
    return 1 if stale else 0


if __name__ == "__main__":
    sys.exit(main())
