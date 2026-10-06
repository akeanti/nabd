import csv
from decimal import Decimal
from pathlib import Path

import pytest

BOM_PATH = Path(__file__).resolve().parents[2] / "hardware" / "BOM.csv"


def read_bom() -> list[dict[str, str]]:
    with BOM_PATH.open(newline="", encoding="utf-8") as bom:
        return list(csv.DictReader(bom))


def item_rows() -> list[dict[str, str]]:
    return [row for row in read_bom() if not row["item"].startswith("total_")]


def total_row(item: str) -> Decimal:
    (row,) = (row for row in read_bom() if row["item"] == item)
    return Decimal(row["line_cost_usd"])


@pytest.mark.parametrize("row", item_rows(), ids=lambda row: row["item"])
def test_line_cost_is_quantity_times_unit_cost(row: dict[str, str]) -> None:
    expected = Decimal(row["quantity"]) * Decimal(row["unit_cost_usd"])

    assert Decimal(row["line_cost_usd"]) == expected


def test_tier_totals_sum_their_items() -> None:
    common = sum(
        (Decimal(row["line_cost_usd"]) for row in item_rows() if row["tier"] == "common"),
        Decimal(0),
    )
    tier_b_only = sum(
        (Decimal(row["line_cost_usd"]) for row in item_rows() if row["tier"] == "B"),
        Decimal(0),
    )

    assert total_row("total_a") == common
    assert total_row("total_b") == common + tier_b_only
