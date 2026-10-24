# Evaluation report

## Current status
This scaffold validates the output format and row count, but its decision engine is not yet a complete evidence-based auditor. It is not appropriate to claim measured case-level, field-level, or sequence accuracy until it is evaluated against `dataset/sample_output.csv`.

## Required evaluation
1. Compare generated output for every sample request against `sample_output.csv`.
2. Report case-level status accuracy.
3. Compare each JSON step field and ordered sequence.
4. Add at least three independently authored cases:
   - no deletion request / explicit cancellation;
   - active sync flow can recreate an otherwise deleted record;
   - retained audit record contains direct PII and must be redacted while the record remains.
5. Document failures found and improvements made.

## Known gaps
- Evidence parsing currently reads text-readable formats only; image/PDF evidence needs OCR or document parsing.
- Resource state at `audit_at` is not yet reconstructed from all event histories.
- The decision engine must generate the complete ordered findings/remediation/verification plan and cite evidence IDs.
