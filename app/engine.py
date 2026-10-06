from .dependency import resolve_dependencies
from .translator import translate_formula
from .validator import validate_dax
from .visual_mapper import map_visual
from .confidence import (
    calculate_confidence,
    generate_confidence_reasons
)


def find_calculation(calculations, name):

    for calculation in calculations:

        if calculation["name"] == name:
            return calculation

    raise ValueError(
        f"Calculation '{name}' not found"
    )


def migrate(data):

    
    calculations = data["calculations"]

    
    dependency_order = resolve_dependencies(
        calculations
    )

    
    translated = {}

    for name in dependency_order:

        calculation = find_calculation(
            calculations,
            name
        )

        formula = calculation["formula"]

        translated[name] = translate_formula(
            formula
        )

    
    target_name = data["target_calculation"]

    target = find_calculation(
        calculations,
        target_name
    )

    source_formula = target["formula"]

    validation = validate_dax(
        source_formula,
        data["existing_dax"]
    )

    
    visual_mapping = map_visual(
        data["visual"]
    )

    
    dependency_resolved = (
        len(dependency_order) == len(calculations)
    )

    translation_success = (
        len(translated) == len(calculations)
    )

    visual_supported = (
        visual_mapping != "Needs manual review"
    )

    
    ambiguity = 0

    for calculation in calculations:

        formula = calculation["formula"].upper()

        if "WINDOW_SUM" in formula:
            ambiguity += 1

        if "RUNNING_SUM" in formula:
            ambiguity += 1

    
    ambiguity = min(
        ambiguity,
        1
    )


    confidence = calculate_confidence(
        dependency_resolved=dependency_resolved,
        translation_success=translation_success,
        validation_score=validation["validation_score"],
        visual_supported=visual_supported,
        ambiguity=ambiguity
    )



    confidence_reasons = generate_confidence_reasons(
        dependency_resolved=dependency_resolved,
        translation_success=translation_success,
        is_corrected=validation["is_corrected"],
        visual_supported=visual_supported,
        ambiguity=ambiguity
    )

   

    return {

        "dependency_order": dependency_order,

        "translated_calculations": translated,

        "predicted_dax": validation[
            "corrected_dax"
        ],

        "visual_mapping": visual_mapping,

        "is_corrected": validation[
            "is_corrected"
        ],

        "validation_score": validation[
            "validation_score"
        ],

        "reason": validation[
            "reason"
        ],

        "confidence_score": confidence[
            "score"
        ],

        "confidence_level": confidence[
            "level"
        ],

        "confidence_reasons": confidence_reasons
    }