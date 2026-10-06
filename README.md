# Office Soln AI BI Migration Engine

## 1. Objective

This project converts Tableau-style calculations into DAX expressions for Power BI and other BI workflows. The goal is to support a practical, explainable migration pipeline that preserves business logic as closely as possible while highlighting unsupported or approximated behaviors.

## 2. Problem Statement

Organizations often build complex KPI logic in Tableau using calculated fields, fixed LODs, table calculations, and conditional expressions. Translating these formulas to DAX is difficult because the syntax and evaluation model differ across tools. This engine aims to automate the most common Tableau patterns and provide validation, confidence scoring, and output structure suitable for migration review.

## 3. Approach

The migration process is structured as a staged pipeline:

1. Parse Tableau formulas and identify supported constructs.
2. Resolve dependencies between calculations.
3. Translate supported logic into DAX-like expressions.
4. Validate the translated output against the target DAX pattern.
5. Detect unsupported constructs and flag them for manual review.
6. Score the confidence of the result and present the translated output and reasoning.

## 4. Architecture

The system is organized into modular components:

- `app/parser.py` — parses Tableau formulas into identifiable expressions
- `app/translator.py` — translates Tableau functions and syntax to DAX patterns
- `app/dependency.py` — resolves dependency ordering between calculations
- `app/validator.py` — validates and corrects generated DAX output
- `app/visual_mapper.py` — maps Tableau visual structures to supported DAX outputs
- `app/confidence.py` — calculates confidence and generates justification reasons
- `app/engine.py` — coordinates the end-to-end migration workflow
- `app/api.py` — exposes the migration engine over a Flask API
- `app/benchmark.py` — evaluates translation quality against benchmarks
- `data/` — sample and benchmark inputs
- `tests/` — automated regression and API tests

## 5. Design Decisions

- Keep the translation engine intentionally pragmatic and source-driven rather than fully exhaustive.
- Support the most common Tableau patterns first: aggregations, IF logic, fixed LODs, window sums, and running sums.
- Maintain a transparent output object with translated values, validation status, and confidence reasons.
- Surface approximation and limitation notes explicitly rather than silently producing incorrect DAX.
- Keep the API lightweight so the migration workflow can be tested and integrated easily.

## 6. Supported Tableau Expressions

The project currently supports a focused subset of Tableau expressions, including:

- `SUM([Sales])`
- `AVG([Sales])`
- `MIN(...)`, `MAX(...)`, `COUNT(...)`
- `IF ... THEN ... ELSE ... END`
- `{FIXED [Region]: SUM([Sales])}`
- `WINDOW_SUM(SUM([Profit]))`
- `RUNNING_SUM(SUM([Sales]))`

These are converted into DAX equivalents where possible, with approximate handling for expressions that require Tableau context semantics.

## 7. Dependency Resolution

Calculation dependency resolution ensures formulas are translated in the correct order. If one calculation references another, the engine resolves the dependency graph before generating DAX. This reduces errors caused by undefined order and protects nested metrics.

## 8. DAX Validation & Correction

After translation, the engine validates the generated DAX output against the existing structure and expected patterns. If the generated output is incomplete or semantically weak, it attempts correction and returns the corrected DAX plus validation metadata.

This stage includes:

- validation score generation
- corrected DAX output
- explanatory reasoning
- detection of likely semantic drift

## 9. Visual Mapping

The engine also maps the source visual configuration into a consistent output structure. For example, it tracks:

- visual type
- dimensions
- measures
- compatibility with supported output patterns

This helps identify whether the translated formula can be used in a corresponding Power BI visual without manual intervention.

## 10. Confidence Scoring

Each migration result receives a confidence score that reflects the reliability of the translated output. The score is informed by:

- dependency completeness
- successful translation coverage
- DAX validation quality
- visual compatibility
- ambiguity caused by Tableau constructs such as window and running calculations

The result includes both a score and a human-readable explanation.

## 11. Benchmark / Evaluation

The benchmark layer evaluates translation quality against representative sample formulas and expected DAX outputs. It helps confirm whether the engine behaves consistently across common migration tasks and can be improved incrementally.

## 12. Before vs After Accuracy

Translating Tableau logic to DAX is not always a strict one-to-one conversion. Some expressions require approximation because Tableau semantics depend on partitioning, aggregation context, and hidden metadata. This project documents these differences and exposes them in the output so users understand when the engine is producing a near-equivalent result rather than an exact match.

## 13. Sample Output

A sample migration response includes:

- dependency order
- translated calculations
- predicted DAX
- visual mapping
- validation status
- confidence score
- confidence reasons

Example result structure:

```json
{
  "success": true,
  "result": {
    "predicted_dax": "SUM(Sales) / SUM(Profit)",
    "is_corrected": true,
    "confidence_score": 0.92,
    "confidence_level": "high"
  }
}
```

## 14. Error Analysis

The project tracks issues and edge cases separately so unsupported formulas are not silently accepted. This includes handling for:

- unsupported nested Tableau functions
- ambiguous calculation semantics
- partial DAX equivalence
- cases requiring manual review

## 15. Limitations

This is a pragmatic prototype for Tableau-to-DAX translation. It does not attempt to fully implement a complete Tableau parser or a full semantic model of every Tableau function.

The main limitations are:

- Deeply nested expressions may require approximation.
- Table calculation behavior depends on context metadata.
- Advanced Tableau partitioning and ordering may not be fully representable in DAX without additional domain logic.
- Some formulas need human review for exact business equivalence.

## 16. Future Improvements

Planned enhancements include:

- broader Tableau function coverage
- better handling of nested calculations
- stronger validation heuristics
- richer benchmark datasets
- improved API schema documentation
- UI-based formula testing and inspection

## 17. Installation

1. Clone the repository.
2. Create a virtual environment.
3. Install dependencies:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

On Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## 18. API Usage

The service exposes a migration endpoint:

- `POST /api/migrate`

Example request body:

```json
{
  "calculations": [
    {
      "name": "KPI_1",
      "formula": "SUM([Profit]) / SUM([Sales])"
    }
  ],
  "target_calculation": "KPI_1",
  "existing_dax": "SUM(Sales) / SUM(Profit)",
  "visual": {
    "visual_type": "bar",
    "dimensions": ["Region"],
    "measures": ["KPI_1"]
  }
}
```

Health check:

- `GET /api/health`

## 19. Testing

To run the project tests:

```bash
pytest
```

The project includes API, translator, benchmark, validator, and confidence tests to keep the migration logic stable and regression-safe.

---

This README documents the project goals, pipeline, supported expression patterns, and current limitations in a format suitable for technical review and project onboarding.
