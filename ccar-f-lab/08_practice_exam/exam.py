"""Interactive practice exam: per-question explanations, per-domain scoring, weak-domain report, history."""
import json, random, sys, csv, datetime, pathlib, collections
HERE = pathlib.Path(__file__).parent
Q = json.loads((HERE / "questions.json").read_text())
if "--domain" in sys.argv:
    k = sys.argv[sys.argv.index("--domain") + 1].lower(); Q = [q for q in Q if k in q["domain"].lower()]
review = "--review" in sys.argv
random.shuffle(Q)
score = collections.defaultdict(lambda: [0, 0]); mod = {}
for i, q in enumerate(Q, 1):
    print(f"\n[{i}/{len(Q)}] ({q['domain']})\n{q['stem']}"); [print("  " + o) for o in q["options"]]
    ans = q["answer"] if review else input("Your answer (A-D): ").strip().upper()[:1]
    ok = ans == q["answer"]; score[q["domain"]][0] += ok; score[q["domain"]][1] += 1; mod[q["domain"]] = q["module"]
    print(("✅ Correct" if ok else f"❌ Incorrect — answer {q['answer']}") + f"\n  Why: {q['explanation']}")
    for k, v in q["distractors"].items(): print(f"  {k} wrong: {v}")
print("\n=== Results by domain ===")
tot = [0, 0]; weak = []
for d, (c, n) in sorted(score.items()):
    pct = 100 * c / n; tot[0] += c; tot[1] += n; flag = "  <-- WEAK" if pct < 80 else ""
    print(f"{d:32} {c}/{n}  {pct:5.0f}%{flag}")
    if pct < 80: weak.append(f"{d} (redo module {mod[d]})")
print(f"{'OVERALL':32} {tot[0]}/{tot[1]}  {100*tot[0]/max(tot[1],1):5.0f}%")
print("Weak domains:", ", ".join(weak) or "none — retest in 3 days")
if not review:
    with open(HERE / "history.csv", "a", newline="") as f:
        w = csv.writer(f); [w.writerow([datetime.date.today(), d, c, n]) for d, (c, n) in score.items()]
