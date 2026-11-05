"""Checks that the headline figures printed in business-case.md match financial_model.py. Run: python3 test_document.py"""
import os
import financial_model as m

doc = open(os.path.join(os.path.dirname(__file__), "..", "business-case.md"), encoding="utf-8").read()
p = m.INPUTS
failures = 0




def eur(x):
    return f"€{round(x, -3):,.0f}"


def check(label, text):
    global failures
    ok = text in doc
    print(("PASS  " if ok else "FAIL  ") + label + ("" if ok else f"   expected to find: {text}"))
    failures += 0 if ok else 1


for name, r in (("pessimistic", 0.5), ("base", 0.75), ("optimistic", 1.0)):
    s = m.scenario(p, r)
    check(f"{name} NPV", eur(s["npv"]))
    check(f"{name} IRR", f"{s['irr']*100:.0f}%")
    check(f"{name} payback", f"{s['payback_months']:.0f} months")
base = m.scenario(p, 0.75)
check("TCO", eur(base["tco"]))
check("ROI", f"{base['roi']*100:.0f}%")
check("net benefit", eur(base["net_benefit"]))
check("exact NPV in the table", f"€{base['npv']:,.0f}")
check("costs +20% NPV", eur(m.scenario(p, 0.75, cost_multiplier=1.2)["npv"]))
check("prep-only NPV", eur(m.scenario(p, 0.75, exclude=("deal_acceleration", "follow_up", "onboarding"))["npv"]))
check("break-even", f"{m.break_even_realisation(p)*100:.0f}% of the modelled benefit")
for stale in ("€980,000", "227%", "€339,000", "€319,000", "10-month", "180,000 years"):
    ok = stale not in doc
    print(("PASS  " if ok else "FAIL  ") + f"no stale figure: {stale}")
    failures += 0 if ok else 1
print("\nALL PASSED" if not failures else f"\n{failures} FAILED")
raise SystemExit(1 if failures else 0)
