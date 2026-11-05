# Commercial Intelligence AI Assistant: a business-case framework

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

## What this shows

- **Numbers that stand up.** Every figure in the document comes from a tested financial model in Python ([model/](model)). A second test reads the document and checks the text matches the model — the two cannot drift apart.
- **Staged commitment, not a leap.** €15k readiness sprint → €94k pilot → €255k scale, with Day 45 and Day 90 gates. Maximum loss is capped at €109k, not €364k.
- **Readiness plan that admits what's missing.** The [prep/](prep) folder marks each check as Done, Drafted or Open — including "no sponsor yet" and "AI Owner role not filled". Honest about what still needs to be proven.
- **Governance and ethics as first-class.** Specific policies with named owners: 1-in-20 hallucination rate pauses the feature, prompt-injection tests in Phase 0, EU AI Act classification confirmed by Legal.
- **Framework thinking.** Designed to be adapted (see [How to adapt this for your company](#how-to-adapt-this-for-your-company)).

## Where to start

1. The executive summary at the top of [business-case.md](business-case.md) (two minutes).
2. The model in [model/](model): change an input and the figures update.
3. The slide deck, then [prep/](prep) for how to get a proposal ready for a decision.

## What is here

| File | What it is |
|---|---|
| [business-case.md](business-case.md) | The full business case: problem, strategy, costs, benefits, phases and gates, governance, risk, ethics |
| [model/financial_model.py](model/financial_model.py) | The financial model in plain Python. Every figure in the business case comes from it |
| [model/test_financial_model.py](model/test_financial_model.py) and [model/test_document.py](model/test_document.py) | Tests: the model reproduces the figures, and the numbers printed in the document match the model |
| [prep/](prep) | A readiness plan: a status-marked checklist, the questions a leader is likely to ask, and a baseline template. Open items are marked as open |
| [Dhankar_Ajay_AI_Business_Case_slides.pdf](Dhankar_Ajay_AI_Business_Case_slides.pdf) | The slide deck (23 main + 7 backup slides), previewable on GitHub |
| [speaker-notes.md](speaker-notes.md) | A corrected talk script |

## Run the model

```bash
cd model && python3 financial_model.py && python3 test_financial_model.py && python3 test_document.py
