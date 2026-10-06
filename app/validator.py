import re

from .translator import translate_formula


def normalize_dax(dax):

    return re.sub(
        r"\s+",
        "",
        dax.upper()
    )


def detect_reversed_ratio(
    source_formula,
    existing_dax
):

    source = source_formula.upper()
    existing = normalize_dax(existing_dax)

    

    source_has_profit_sales = (
        "SUM([PROFIT])" in source
        and
        "SUM([SALES])" in source
    )

    existing_is_reversed = (
        "SUM(SALES)/SUM(PROFIT)" in existing
    )

    return (
        source_has_profit_sales
        and existing_is_reversed
    )


def validate_dax(
    source_formula,
    existing_dax
):

    expected_dax = translate_formula(
        source_formula
    )

    normalized_existing = normalize_dax(
        existing_dax
    )

    normalized_expected = normalize_dax(
        expected_dax
    )

    if normalized_existing == normalized_expected:

        return {
            "is_correct": True,
            "is_corrected": False,
            "corrected_dax": existing_dax,
            "reason": "Existing DAX matches the translated Tableau logic.",
            "validation_score": 1.0
        }

    if detect_reversed_ratio(
        source_formula,
        existing_dax
    ):

        return {
            "is_correct": False,
            "is_corrected": True,
            "corrected_dax": expected_dax,
            "reason": "Numerator and denominator are reversed.",
            "validation_score": 0.1
        }

    
    return {
        "is_correct": False,
        "is_corrected": True,
        "corrected_dax": expected_dax,
        "reason": "Existing DAX does not match the translated Tableau logic.",
        "validation_score": 0.4
    }