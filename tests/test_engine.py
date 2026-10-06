"""Tests for the formula translation engine."""

from app.translator import (
    translate_formula,
    translate_window_sum,
    translate_running_sum,
)


def test_translate_sum():
    """Verify SUM translation."""

    assert (
        translate_formula("SUM([Sales])")
        == "SUM(Sales)"
    )


def test_translate_avg():
    """Verify AVG translation."""

    assert (
        translate_formula("AVG([Sales])")
        == "AVERAGE(Sales)"
    )


def test_translate_if():
    """Verify IF/THEN/ELSE translation."""

    formula = (
        "IF [B] > 0.2 "
        "THEN 'High' "
        "ELSE 'Low' "
        "END"
    )

    expected = (
        "IF(B > 0.2, 'High', 'Low')"
    )

    assert translate_formula(formula) == expected


def test_translate_fixed_lod():
    """Verify FIXED LOD translation."""

    formula = (
        "{FIXED [Region]: SUM([Sales])}"
    )

    expected = (
        "CALCULATE("
        "SUM(Sales), "
        "ALLEXCEPT("
        "'Data', "
        "'Data'[Region]"
        ")"
        ")"
    )

    assert translate_formula(formula) == expected


def test_translate_window_sum():
    """Verify WINDOW_SUM translation."""

    formula = (
        "WINDOW_SUM(SUM([Profit]))"
    )

    expected = (
        "CALCULATE("
        "SUM(Profit), "
        "ALLSELECTED('Data')"
        ")"
    )

    assert (
        translate_window_sum(formula)
        == expected
    )


def test_translate_running_sum():
    """Verify RUNNING_SUM translation."""

    formula = (
        "RUNNING_SUM(SUM([Sales]))"
    )

    expected = (
        "CALCULATE("
        "SUM(Sales), "
        "ALLSELECTED('Data')"
        ")"
    )

    assert (
        translate_running_sum(formula)
        == expected
    )