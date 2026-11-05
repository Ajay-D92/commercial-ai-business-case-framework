"""Three-year financial model for the Commercial Intelligence AI Assistant business case.

Pure Python, no dependencies. Every number in the business case comes from here.
Run:  python3 financial_model.py
"""

# ---- inputs -------------------------------------------------------------------------------------------------------
INPUTS = {
    # rep time
    "rate_per_hour": 75,                 # fully loaded EUR per hour
    "calls_per_rep_week": 7,             # prepared client calls per rep per week at scale (assumption, validate in Phase 0)
    "prep_now_min": 105,                 # current average prep minutes per call (midpoint of 90-120)
    "prep_target_min": 20,               # target prep minutes per call after full deployment
    "pilot_reduction": 0.25,             # prep time reduction achieved in the pilot
    "pilot_weeks": 13,
    "scaled_weeks_y1": 27,               # operative weeks after the pilot inside the 40-week year-1 model
    "model_weeks": 40,
    "pilot_hours_per_week": 3,           # stated in the business case (checked against the inputs above in the tests)
    "scaled_hours_per_week": 10,         # stated in the business case (checked against the inputs above in the tests)
    "reps": {1: 5, 2: 12, 3: 18},
    # other benefits (gross, 100% realisation) - assumptions to be validated in the pilot
    "deal_acceleration": {1: 60_000, 2: 180_000, 3: 270_000},   # extra closed deals x EUR 30,000 margin (2, 6, 9 deals)
    "follow_up": {1: 0, 2: 40_000, 3: 0},
    "onboarding": {1: 0, 2: 0, 3: 80_000},
    # costs
    "phase0": 15_000,
    "phase1": 94_000,
    "infrastructure": 20_000,
    "llm_api": 45_000,
    "continuous_development": 25_000,
    "ai_owner_fte": 0.5,
    "ai_owner_months": 33,               # months 4 to 36
    "ai_owner_cost_per_fte_year": 120_000,
    "discount_rate": 0.12,
}


def prep_hours_y1(p):
    """Blended weekly hours saved per rep in year 1, rounded to one decimal as in the business case."""
    blended = (p["pilot_weeks"] * p["pilot_hours_per_week"] + p["scaled_weeks_y1"] * p["scaled_hours_per_week"]) / p["model_weeks"]
    return round(blended, 1)


def gross_benefits(p):
    """Gross yearly benefit lines at 100% realisation."""
    out = {}
    for y in (1, 2, 3):
        hours = prep_hours_y1(p) if y == 1 else p["scaled_hours_per_week"]
        prep = p["reps"][y] * hours * p["rate_per_hour"] * p["model_weeks"]
        out[y] = {
            "prep_time": prep,
            "deal_acceleration": p["deal_acceleration"][y],
            "follow_up": p["follow_up"][y],
            "onboarding": p["onboarding"][y],
        }
        out[y]["total"] = sum(out[y].values())
    return out


def costs(p):
    owner_ongoing = p["ai_owner_fte"] * p["ai_owner_months"] / 12 * p["ai_owner_cost_per_fte_year"]
    ongoing = p["infrastructure"] + p["llm_api"] + owner_ongoing + p["continuous_development"]
    return {
        "year0": p["phase0"] + p["phase1"],
        "ai_owner_ongoing": owner_ongoing,
        "phase2_3": ongoing,
        "per_year": ongoing / 3,
        "tco": p["phase0"] + p["phase1"] + ongoing,
    }


def npv(rate, flows):
    return sum(f / (1 + rate) ** t for t, f in enumerate(flows))


def irr(flows):
    lo, hi = -0.99, 10.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if npv(mid, flows) > 0:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def payback_months(flows):
    """Months until cumulative undiscounted cash flow turns positive; the initial cost sits at month 0."""
    cumulative = flows[0]
    for t in range(1, len(flows)):
        if cumulative + flows[t] >= 0:
            return 12 * (t - 1) + 12 * (-cumulative) / flows[t]
        cumulative += flows[t]
    return None


def scenario(p, realisation, cost_multiplier=1.0, exclude=()):
    g = gross_benefits(p)
    c = costs(p)
    benefits = []
    for y in (1, 2, 3):
        total = sum(v for k, v in g[y].items() if k != "total" and k not in exclude)
        benefits.append(total * realisation)
    year0 = c["year0"] * cost_multiplier
    yearly = c["per_year"] * cost_multiplier
    flows = [-year0] + [b - yearly for b in benefits]
    total_cost = year0 + 3 * yearly
    benefit_total = sum(benefits)
    pb = payback_months(flows)
    return {
        "realisation": realisation,
        "benefits": benefits,
        "flows": flows,
        "npv": npv(p["discount_rate"], flows),
        "irr": irr(flows),
        "payback_months": pb,
        "tco": total_cost,
        "net_benefit": benefit_total - total_cost,
        "roi": (benefit_total - total_cost) / total_cost,
    }


def break_even_realisation(p, **kw):
    lo, hi = 0.0, 1.0
    for _ in range(100):
        mid = (lo + hi) / 2
        if scenario(p, mid, **kw)["npv"] > 0:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2


def fmt(s):
    pb = "n/a" if s["payback_months"] is None else f"{s['payback_months']:.0f}"
    return f"NPV EUR {s['npv']:,.0f} | IRR {s['irr']*100:.0f}% | payback {pb} months | ROI {s['roi']*100:.0f}% | net benefit EUR {s['net_benefit']:,.0f}"


def report(p=INPUTS):
    c = costs(p)
    print(f"Costs: Phase 0+1 EUR {c['year0']:,.0f} | Phase 2-3 EUR {c['phase2_3']:,.0f} (AI owner EUR {c['ai_owner_ongoing']:,.0f}) | TCO EUR {c['tco']:,.0f} | per year EUR {c['per_year']:,.0f}")
    g = gross_benefits(p)
    for y in (1, 2, 3):
        print(f"Year {y} gross benefit EUR {g[y]['total']:,.0f}  " + ", ".join(f"{k} {v:,.0f}" for k, v in g[y].items() if k != 'total'))
    print("Gross 3-year benefit EUR", f"{sum(g[y]['total'] for y in (1, 2, 3)):,.0f}")
    for r, name in ((0.5, "Pessimistic 50%"), (0.75, "Base 75%"), (1.0, "Optimistic 100%")):
        print(f"{name:16s}", fmt(scenario(p, r)))
    print("\nStress tests on the base case (75%):")
    print("Costs +20%        ", fmt(scenario(p, 0.75, cost_multiplier=1.2)))
    print("Prep time only    ", fmt(scenario(p, 0.75, exclude=("deal_acceleration", "follow_up", "onboarding"))))
    print("Break-even realisation:", f"{break_even_realisation(p)*100:.0f}% of modelled benefit")
    print("Break-even, prep time only:", f"{break_even_realisation(p, exclude=('deal_acceleration','follow_up','onboarding'))*100:.0f}%")


if __name__ == "__main__":
    report()
