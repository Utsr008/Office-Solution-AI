"""Tests for benchmark evaluation."""

from app.benchmark import run_benchmark


def test_benchmark():
    """Verify that all benchmark cases are evaluated."""

    result = run_benchmark(
        "data/benchmark_cases.json"
    )

    assert result["total_cases"] == 10
    assert result["before_accuracy"] >= 0
    assert result["after_accuracy"] >= 0
    assert len(result["results"]) == 10