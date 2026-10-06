import json
import re

from .engine import migrate


def normalize(value):

    return re.sub(
        r"\s+",
        "",
        value.upper()
    )


def is_correct(actual, expected):

    return (
        normalize(actual)
        ==
        normalize(expected)
    )


def run_benchmark(benchmark_file):

    with open(
        benchmark_file,
        "r",
        encoding="utf-8"
    ) as f:

        cases = json.load(f)

    before_correct = 0
    after_correct = 0

    results = []

    for case in cases:


        before = is_correct(
            case["existing_dax"],
            case["expected_dax"]
        )

        if before:
            before_correct += 1

        data = {
            "calculations": [
                {
                    "name": "BenchmarkCalculation",
                    "formula": case["source_formula"]
                }
            ],

            "target_calculation":
                "BenchmarkCalculation",

            "existing_dax":
                case["existing_dax"],

            "visual": {
                "visual_type": "bar",
                "dimensions": [],
                "measures": [
                    "BenchmarkCalculation"
                ]
            }
        }

        try:

            result = migrate(data)

            predicted = result[
                "predicted_dax"
            ]

            after = is_correct(
                predicted,
                case["expected_dax"]
            )

            if after:
                after_correct += 1

            results.append({

                "id": case["id"],

                "name": case["name"],

                "before_correct": before,

                "after_correct": after,

                "predicted_dax": predicted,

                "expected_dax":
                    case["expected_dax"],

                "confidence_score":
                    result["confidence_score"],

                "confidence_level":
                    result["confidence_level"],

                "reason":
                    result["reason"]

            })

        except (KeyError, TypeError, ValueError) as error:


            results.append({

                "id": case["id"],

                "name": case["name"],

                "before_correct": before,

                "after_correct": False,

                "predicted_dax": None,

                "expected_dax":
                    case["expected_dax"],

                "confidence_score": 0,

                "confidence_level": "LOW",

                "reason":
                    f"Error: {error}"

            })

    total = len(cases)

    before_accuracy = (
        before_correct / total
        if total
        else 0
    )

    after_accuracy = (
        after_correct / total
        if total
        else 0
    )

    improvement = (
        after_accuracy -
        before_accuracy
    )

    return {

        "total_cases": total,

        "before_correct":
            before_correct,

        "after_correct":
            after_correct,

        "before_accuracy":
            round(
                before_accuracy * 100,
                2
            ),

        "after_accuracy":
            round(
                after_accuracy * 100,
                2
            ),

        "improvement":
            round(
                improvement * 100,
                2
            ),

        "results": results
    }


def print_benchmark_report(report):

    print()

    print("=" * 60)

    print(
        "BI MIGRATION ACCURACY BENCHMARK"
    )

    print("=" * 60)

    print(
        f"Total Cases       : "
        f"{report['total_cases']}"
    )

    print(
        f"Before Accuracy   : "
        f"{report['before_accuracy']}%"
    )

    print(
        f"After Accuracy    : "
        f"{report['after_accuracy']}%"
    )

    print(
        f"Improvement       : "
        f"{report['improvement']} "
        f"percentage points"
    )

    print("-" * 60)

    for result in report["results"]:

        status = (
            "PASS"
            if result["after_correct"]
            else "FAIL"
        )

        print(
            f"{result['id']:02d}. "
            f"{result['name']:<25} "
            f"{status}"
        )

    print("=" * 60)