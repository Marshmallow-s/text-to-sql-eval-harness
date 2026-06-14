# Text-to-SQL Evaluation Harness

A systematic evaluation framework for text-to-SQL models, built on a custom gold set with execution-accuracy scoring, error taxonomy, and inter-annotator agreement measurement.

## What This Project Does

Large language models can generate SQL from natural language — but how do you know if the SQL is actually correct? This project builds an evaluation harness that:

- Runs model-generated SQL against a verified gold set
- Compares result sets (not just text similarity) to determine correctness
- Classifies errors into a taxonomy (schema errors, join errors, aggregation errors, hallucinated columns)
- Measures annotation consistency using Cohen's kappa

## Project Structure

```
text-to-sql-eval-harness/
├── data/               # Gold set: NL questions + verified SQL answers
├── harness/            # Execution-accuracy evaluation engine
├── analysis/           # Error taxonomy + per-tier scorecard
├── annotation/         # Inter-annotator agreement (Cohen's kappa)
└── db/                 # SQLite database for evaluation
```

## Evaluation Approach

### Gold Set
30 natural language questions with human-verified SQL answers, across three difficulty tiers:
- **Easy (10):** Single table, WHERE, ORDER BY, LIMIT
- **Medium (10):** JOIN, GROUP BY, HAVING, subqueries
- **Hard (10):** Nested subqueries, window functions, multi-table joins

### Execution Accuracy
Model-generated SQL and gold SQL are both executed against the same database. Correctness is determined by comparing result sets — not text similarity. This catches cases where different SQL syntax produces identical results.

### Error Taxonomy
Failed queries are classified by error type to identify systematic model weaknesses.

### Inter-Annotator Agreement
Gold set annotations are independently verified by two annotators. Cohen's kappa measures label consistency.

## Status

🚧 In progress