"""Tests for DAX validation and correction."""

from app.validator import validate_dax


def test_reversed_ratio():
    """Detect and correct reversed numerator and denominator."""

    source = "SUM([Profit]) / SUM([Sales])"
    existing = "SUM(Sales) / SUM(Profit)"

    result = validate_dax(
        source,
        existing,
    )

    assert result["is_correct"] is False
    assert result["is_corrected"] is True

    assert "Profit" in result["corrected_dax"]
    assert "Sales" in result["corrected_dax"]


def test_correct_dax():
    """Verify already-correct DAX."""

    source = "SUM([Profit])"
    existing = "SUM(Profit)"

    result = validate_dax(
        source,
        existing,
    )

    assert result["is_correct"] is True
    assert result["is_corrected"] is False