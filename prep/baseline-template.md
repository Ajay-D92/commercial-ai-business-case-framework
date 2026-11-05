# One-page baseline

Fill this in with measured numbers before presenting. It replaces estimates with our own data. The right-hand column shows which input of the financial model each number changes.

Date measured: ________    Measured by: ________    Sample: ________

| Measure | Value in the model today | How to measure it | Source | Result | Used in the model as |
|---|---|---|---|---|---|
| CRM completeness | Not measured | Share of active deals with the 8 required fields filled | CRM export | ____ % | Phase 0 gate (needs 75% or more) |
| Prep time per call | 105 min (assumption) | Time five reps for three calls each, from opening the account to ending preparation | Stopwatch or rep log | ____ min | `prep_now_min` (currently 105) |
| Prepared calls per rep per week | 7 (assumption) | Count client calls in the last 8 weeks and divide by weeks and reps | CRM or call recordings | ____ | `calls_per_rep_week` (currently 7) |
| Follow-up completion | 37% (reported) | Share of calls followed up within the agreed time | CRM | ____ % | Year 2 follow-up benefit (37% now) |
| Deal cycle | 42 days (reported) | Average days from first meeting to close, last 12 months | CRM | ____ days | Deal-acceleration benefit (42 now) |
| New-joiner ramp time | 6-9 months (reported) | Months from start date to first closed deal, last 4 hires | CRM and HR | ____ months | Onboarding benefit (6-9 now) |
| Informal escalations | Not measured | Questions a week that juniors send to seniors | Short survey | ____ | Adoption target (down 30%) |

## How to use the result

1. Open `model/financial_model.py` and change the matching values at the top (`INPUTS`).
2. Run the model and the tests:

```bash
cd model && python3 financial_model.py && python3 test_financial_model.py
```

3. If the base-case NPV stays positive, say so on the slide. If a number moves a lot, say that too, and show the stress test.
4. If the figures in `business-case.md` no longer match the model, `python3 test_document.py` fails. Update the text to the new figures.

## Decision rule
Write down, before measuring, the result that would make you stop. For example: "If CRM completeness is under 50%, or prep time is under 45 minutes, I will not ask for Phase 0 yet."

Stop number: ________
