# Commercial Intelligence AI Assistant: a business-case framework

[![tests](https://github.com/Ajay-D92/commercial-ai-business-case-framework/actions/workflows/tests.yml/badge.svg)](https://github.com/Ajay-D92/commercial-ai-business-case-framework/actions/workflows/tests.yml)

A worked example of a Phase 1 proof-of-concept business case for an AI assistant that captures and shares the commercial and cross-cultural knowledge held by sales representatives. Written as a template other companies can adapt.

> **About the figures.** This is a framework. Company identifiers have been removed, and operational metrics (deal cycle, follow-up rate, preparation time, inefficiency cost, deal margin) have been replaced with illustrative figures that match the shape of the original data but do not disclose it. The financial model, method and conclusions are unchanged, so the structure can be reused by any company in a similar position.

**The idea in one line:** start with a €15,000 readiness sprint and a €94,000 pilot, with hard gates that cap the loss at €109,000, before committing to a €364,000 three-year build.

| Metric (base case, 75% benefit realisation) | Value |
|---|---|
| NPV (12%) | €626,000 |
| IRR | 153% |
| Payback | 14 months |
| 3-year ROI | 239% |
| 3-year cost | €364,000 |
| Break-even | 25% of the modelled benefit |

## Where to start

1. The executive summary at the top of [business-case.md](business-case.md) (two minutes).
2. The model in [model/](model): change an input and the figures update.
3. [CHANGES.md](CHANGES.md): the errors found in the first version and how each was fixed.
4. The slide deck, then [prep/](prep) for how to get a proposal ready for a decision.

## What is here

| File | What it is |
|---|---|
| [business-case.md](business-case.md) | The full business case: problem, strategy, costs, benefits, phases and gates, governance, risk, ethics |
| [model/financial_model.py](model/financial_model.py) | The financial model in plain Python. Every figure in the business case comes from it |
| [model/test_financial_model.py](model/test_financial_model.py) and [model/test_document.py](model/test_document.py) | Tests: the model reproduces the figures, and the numbers printed in the document match the model |
| [prep/](prep) | A readiness plan: a status-marked checklist, the questions a leader is likely to ask, and a baseline template. Open items are marked as open |
| [CHANGES.md](CHANGES.md) | The inconsistencies found in the first version and how each was fixed |
| [Dhankar_Ajay_AI_Business_Case_slides.pdf](Dhankar_Ajay_AI_Business_Case_slides.pdf) | The slide deck (23 main + 7 backup slides), previewable on GitHub |
| [speaker-notes.md](speaker-notes.md) | A corrected talk script |

## Run the model

```bash
cd model && python3 financial_model.py && python3 test_financial_model.py && python3 test_document.py
```

Change an input at the top of `financial_model.py` (for example `calls_per_rep_week` or `ai_owner_cost_per_fte_year`) and the scenarios and stress tests update.

## How to adapt this for your company

1. Replace the illustrative baseline (deal cycle, follow-up rate, prep time, calls per rep per week, inefficiency cost) with your own numbers in `model/financial_model.py`.
2. Rewrite Section 1.1 of `business-case.md` with your real current state and benchmarks.
3. Re-run the model. The NPV, IRR, payback and ROI update across the document.
4. Use [prep/](prep) to pressure-test whether the proposal is ready for a decision.

## What this shows

How to frame a knowledge-capture AI problem for decision-makers, cost it with stated assumptions, limit exposure with staged gates, plan governance and adoption, and check the numbers with code. It is paired with a working build: the [trend discovery agent](https://github.com/Ajay-D92/e-commerce-trend-discovery-agent) shows the same approach applied end-to-end.

## A note on use

This document is shared as a framework for other companies and practitioners to adapt. It is not licensed for resale or republication. The figures are illustrative; do not cite them as benchmarks.
