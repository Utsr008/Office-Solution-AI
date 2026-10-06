"""Tests for confidence scoring."""

from app.confidence import (
    calculate_confidence,
    generate_confidence_reasons,
)


def test_high_confidence():
    """Verify high-confidence migration results."""

    result = calculate_confidence(
        dependency_resolved=True,
        translation_success=True,
        validation_score=1.0,
        visual_supported=True,
        ambiguity=0,
    )

    assert result["score"] >= 0.85
    assert result["level"] == "HIGH"


def test_low_confidence():
    """Verify low-confidence migration results."""

    result = calculate_confidence(
        dependency_resolved=False,
        translation_success=False,
        validation_score=0.1,
        visual_supported=False,
        ambiguity=1,
    )

    assert result["level"] == "LOW"


def test_confidence_reasons():
    """Verify confidence explanation generation."""

    reasons = generate_confidence_reasons(
        dependency_resolved=True,
        translation_success=True,
        is_corrected=True,
        visual_supported=True,
        ambiguity=0,
    )

    assert len(reasons) >= 3