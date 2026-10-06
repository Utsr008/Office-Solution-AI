import re


AGGREGATIONS = {
    "SUM": "SUM",
    "AVG": "AVERAGE",
    "MIN": "MIN",
    "MAX": "MAX",
    "COUNT": "COUNT"
}


def translate_aggregation(formula):

    pattern = r"(SUM|AVG|MIN|MAX|COUNT)\s*\(\s*\[([^\]]+)\]\s*\)"

    def replace(match):

        function = match.group(1).upper()
        field = match.group(2)

        dax_function = AGGREGATIONS[function]

        return f"{dax_function}({field})"

    return re.sub(
        pattern,
        replace,
        formula,
        flags=re.IGNORECASE
    )

def translate_fields(formula):

    return re.sub(
        r"(?<!')\[([^\]]+)\]",
        r"\1",
        formula
    )


def translate_if(formula):

    pattern = (
        r"IF\s+(.+?)"
        r"\s+THEN\s+(.+?)"
        r"\s+ELSE\s+(.+?)"
        r"\s+END"
    )

    match = re.fullmatch(
        pattern,
        formula.strip(),
        flags=re.IGNORECASE | re.DOTALL
    )

    if not match:
        return formula

    condition = match.group(1)
    true_value = match.group(2)
    false_value = match.group(3)

    return (
        f"IF("
        f"{condition}, "
        f"{true_value}, "
        f"{false_value}"
        f")"
    )


def translate_fixed_lod(formula):

    pattern = (
        r"\{FIXED\s+"
        r"\[([^\]]+)\]\s*:\s*"
        r"(.+?)\}"
    )

    match = re.search(
        pattern,
        formula,
        flags=re.IGNORECASE | re.DOTALL
    )

    if not match:
        return formula

    dimension = match.group(1)
    expression = match.group(2).strip()

    expression = translate_aggregation(expression)

    dax = (
        f"CALCULATE("
        f"{expression}, "
        f"ALLEXCEPT("
        f"'Data', "
        f"'Data'[{dimension}]"
        f")"
        f")"
    )

    return formula.replace(
        match.group(0),
        dax
    )

def translate_window_sum(formula):

    pattern = r"WINDOW_SUM\s*\(\s*(.*?)\s*\)"

    match = re.fullmatch(
        pattern,
        formula.strip(),
        flags=re.IGNORECASE | re.DOTALL
    )

    if not match:
        return formula

    inner = match.group(1).strip()

    # Do NOT call translate_formula() here.
    # Translate only the aggregation inside WINDOW_SUM.
    translated_inner = translate_aggregation(inner)

    return (
        f"CALCULATE("
        f"{translated_inner}, "
        f"ALLSELECTED('Data')"
        f")"
    )

def translate_running_sum(formula):

    pattern = r"RUNNING_SUM\s*\(\s*(.*?)\s*\)"

    match = re.fullmatch(
        pattern,
        formula.strip(),
        flags=re.IGNORECASE | re.DOTALL
    )

    if not match:
        return formula

    inner = match.group(1).strip()

    # Do NOT recursively call translate_formula()
    translated_inner = translate_aggregation(inner)

    return (
        f"CALCULATE("
        f"{translated_inner}, "
        f"ALLSELECTED('Data')"
        f")"
    )


def translate_formula(formula):

    formula = formula.strip()

    # 1. FIXED LOD
    formula = translate_fixed_lod(formula)

    # 2. WINDOW_SUM
    formula = translate_window_sum(formula)

    # 3. RUNNING_SUM
    formula = translate_running_sum(formula)

    # 4. Aggregations
    formula = translate_aggregation(formula)

    # 5. Fields
    formula = translate_fields(formula)

    # 6. IF / THEN / ELSE
    formula = translate_if(formula)

    return formula