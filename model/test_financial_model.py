"""Checks for financial_model.py. Run:  python3 test_financial_model.py"""
import copy
import financial_model as m

failures = 0


def check(label, ok, detail=""):
    global failures
    print(("PASS  " if ok else "FAIL  ") + label + ("" if ok else f"   {detail}"))
    if not ok:
        failures += 1


# --- the original business case is reproduced when the AI owner is priced the way it was --------------------------------
original = copy.deepcopy(m.INPUTS)
original["ai_owner_cost_per_fte_year"] = 120_000 * 12 / (0.5 * 33)    # EUR 120,000 for 0.5 FTE over 33 months
c0 = m.costs(original)
check("original TCO is EUR 319,000", round(c0["tco"]) == 319_000, c0["tco"])
g = m.gross_benefits(original)
check("gross benefits are 175,500 / 580,000 / 890,000", [g[y]["total"] for y in (1, 2, 3)] == [175_500, 580_000, 890_000])
base = m.scenario(original, 0.75)
check("original base NPV is about EUR 662,000", abs(base["npv"] - 662_000) < 1_500, base["npv"])
check("original base IRR is about 163%", abs(base["irr"] - 1.63) < 0.01, base["irr"])
check("original base payback is 14 months", round(base["payback_months"]) == 14, base["payback_months"])
check("original base ROI is about 287%", abs(base["roi"] - 2.87) < 0.01, base["roi"])
check("original pessimistic NPV is about EUR 349,000", abs(m.scenario(original, 0.5)["npv"] - 349_000) < 1_500)
check("original optimistic NPV is about EUR 976,000", abs(m.scenario(original, 1.0)["npv"] - 976_000) < 1_500)
check("original optimistic payback is 12 months (not 10)", round(m.scenario(original, 1.0)["payback_months"]) == 12)

# --- the corrected inputs: one AI owner rate everywhere -------------------------------------------------------------------
p = m.INPUTS
phase1_owner = 0.3 * 3 / 12 * p["ai_owner_cost_per_fte_year"]
check("Phase 1 AI owner line (0.3 FTE x 3 months) is EUR 9,000 at the single rate", round(phase1_owner) == 9_000, phase1_owner)
c = m.costs(p)
check("ongoing AI owner line (0.5 FTE x 33 months) is EUR 165,000 at the same rate", round(c["ai_owner_ongoing"]) == 165_000, c["ai_owner_ongoing"])
check("corrected TCO is EUR 364,000", round(c["tco"]) == 364_000, c["tco"])
check("maximum exposure before the gates is still EUR 109,000", c["year0"] == 109_000)

# --- the rep-time assumptions agree with each other ------------------------------------------------------------------------
saved_scaled = (p["prep_now_min"] - p["prep_target_min"]) * p["calls_per_rep_week"] / 60
saved_pilot = p["prep_now_min"] * p["pilot_reduction"] * p["calls_per_rep_week"] / 60
check("7 calls a week at 85 minutes saved gives about 10 hours a week", abs(saved_scaled - p["scaled_hours_per_week"]) < 0.3, saved_scaled)
check("7 calls a week at a 25% reduction gives about 3 hours a week", abs(saved_pilot - p["pilot_hours_per_week"]) < 0.3, saved_pilot)
check("year-1 blended hours are 7.7", m.prep_hours_y1(p) == 7.7)

# --- scenarios are ordered and the stress tests behave --------------------------------------------------------------------
s50, s75, s100 = (m.scenario(p, r) for r in (0.5, 0.75, 1.0))
check("NPV rises with realisation", s50["npv"] < s75["npv"] < s100["npv"])
check("base case stays positive with costs +20%", m.scenario(p, 0.75, cost_multiplier=1.2)["npv"] > 0)
prep_only = m.scenario(p, 0.75, exclude=("deal_acceleration", "follow_up", "onboarding"))
check("prep-time-only case is smaller than the full base case", prep_only["npv"] < s75["npv"])
check("break-even realisation is below 50%", m.break_even_realisation(p) < 0.5)
check("IRR solves to NPV of zero", abs(m.npv(s75["irr"], s75["flows"])) < 1.0)

print("\nALL PASSED" if failures == 0 else f"\n{failures} FAILED")
raise SystemExit(1 if failures else 0)
