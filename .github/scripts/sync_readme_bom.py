import argparse
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
README = ROOT / "README.md"
BOM = ROOT / "hardware" / "BOM.csv"
START_MARKER = "<!-- bom:start -->"
END_MARKER = "<!-- bom:end -->"


def read_bom() -> list[dict[str, str]]:
    with BOM.open(newline="", encoding="utf-8") as bom:
        return list(csv.DictReader(bom))


def table_row(cells: list[str]) -> str:
    return "| " + " | ".join(cell.replace("|", "\\|") for cell in cells) + " |"


def render_bom(rows: list[dict[str, str]]) -> str:
    totals = {row["item"]: row["line_cost_usd"] for row in rows if row["item"].startswith("total_")}
    lines = [
        "| Build | Estimated cost |",
        "| --- | ---: |",
        f"| Tier A, workshop build | {totals['total_a']} USD |",
        f"| Tier B, precision build | {totals['total_b']} USD |",
        "",
        "<details>",
        "<summary>Every item in <code>hardware/BOM.csv</code></summary>",
        "",
        "| Tier | Quantity | Reference | Part | Example | Line cost (USD) |",
        "| --- | ---: | --- | --- | --- | ---: |",
    ]
    lines += [
        table_row(
            [
                row["tier"],
                row["quantity"],
                row["reference"],
                row["description"],
                row["example_part"],
                row["line_cost_usd"],
            ]
        )
        for row in rows
        if not row["item"].startswith("total_")
    ]
    lines += ["", "</details>"]
    return "\n".join(lines)


def with_bom(readme: str, block: str) -> str:
    start = readme.index(START_MARKER) + len(START_MARKER)
    end = readme.index(END_MARKER)
    return f"{readme[:start]}\n{block}\n{readme[end:]}"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render the bill of materials in README.md from hardware/BOM.csv."
    )
    parser.add_argument("--check", action="store_true", help="fail if README.md is out of date")
    check = parser.parse_args().check
    current = README.read_text(encoding="utf-8")
    expected = with_bom(current, render_bom(read_bom()))
    if current == expected:
        return 0
    if check:
        print(f"README.md: bill of materials is out of date; run {Path(__file__).name}")
        return 1
    README.write_text(expected, encoding="utf-8", newline="\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
