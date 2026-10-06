def calculate_confidence(
    dependency_resolved,
    translation_success,
    validation_score,
    visual_supported,
    ambiguity
):

    score = 0.0

    # Dependency resolution
    if dependency_resolved:
        score += 0.20

    # Translation
    if translation_success:
        score += 0.35

    # Validation
    score += 0.25 * validation_score

    # Visual mapping
    if visual_supported:
        score += 0.10

    # Ambiguity penalty
    score -= 0.10 * ambiguity

    # Keep score between 0 and 1
    score = max(
        0.0,
        min(1.0, score)
    )

    score = round(score, 2)

    if score >= 0.85:
        level = "HIGH"

    elif score >= 0.65:
        level = "MEDIUM"

    else:
        level = "LOW"

    return {
        "score": score,
        "level": level
    }


def generate_confidence_reasons(
    dependency_resolved,
    translation_success,
    is_corrected,
    visual_supported,
    ambiguity
):

    reasons = []

    if dependency_resolved:
        reasons.append(
            "Dependencies resolved successfully"
        )

    if translation_success:
        reasons.append(
            "Tableau formula translated successfully"
        )

    if is_corrected:
        reasons.append(
            "Incorrect existing DAX was detected and corrected"
        )

    if visual_supported:
        reasons.append(
            "Visual type mapped successfully"
        )

    if ambiguity > 0:
        reasons.append(
            "Some ambiguity remains in the source expression"
        )

    return reasons