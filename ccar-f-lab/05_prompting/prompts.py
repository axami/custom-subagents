import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common.client import get_client, MODEL, text_of

AMBIGUOUS = ["Can you increase my VM to 32GB? It's crashing in prod right now.",   # incident disguised as request
             "Please reset MFA for jsmith, he's locked out before the board demo.", # request with urgency
             "Seeing occasional 504s, not sure if it's us."]                         # uncertain incident
FEW_SHOT = """<examples>
<ex><ticket>Need a bigger disk on lnx-dev-03 next sprint.</ticket><label>REQUEST</label><why>Planned change, nothing broken.</why></ex>
<ex><ticket>Need a bigger disk NOW, /var is 100% and orders are failing.</ticket><label>INCIDENT</label><why>Service broken; the "request" is a remediation.</why></ex>
<ex><ticket>Locked out of my account.</ticket><label>REQUEST</label><why>Single-user access issue, standard fulfilment, no service degradation.</why></ex>
<ex><ticket>Intermittent timeouts, unsure if cause is ours.</ticket><label>INCIDENT</label><why>Possible degradation — treat as incident until disproven.</why></ex>
</examples>"""
RUBRIC = """Review criteria (score each PASS/FAIL with one-line reason):
1. Label is INCIDENT if any service is degraded or broken, even if phrased as a request.
2. Rationale cites the specific words that drove the decision.
3. No invented facts (hosts, times) absent from the ticket.
Output: CRITERION n: PASS|FAIL - reason, then FINAL: APPROVE|REVISE"""

def ask(c, system, user):
    return text_of(c.messages.create(model=MODEL, max_tokens=400, system=system, messages=[{"role": "user", "content": user}]))

def zero_shot(c, t): return ask(c, "Classify the ticket as INCIDENT or REQUEST.", f"<ticket>{t}</ticket>")
def few_shot(c, t):  return ask(c, "Classify as INCIDENT or REQUEST. Reply: label + one-line why.", f"{FEW_SHOT}\n<ticket>{t}</ticket>")
def multi_pass(c, t):
    draft = few_shot(c, t)
    review = ask(c, "You are an independent QA reviewer.", f"{RUBRIC}\n<ticket>{t}</ticket>\n<draft>{draft}</draft>")
    if "REVISE" in review:
        draft = ask(c, "Fix the classification using the review.", f"<ticket>{t}</ticket><draft>{draft}</draft><review>{review}</review>")
    return draft, review

if __name__ == "__main__":
    mock = [{"stop_reason": "end_turn", "content": [{"type": "text", "text": "INCIDENT - prod crashing (mock)"}]}]
    c = get_client(mock)
    for t in AMBIGUOUS:
        print("\nTICKET:", t); print(" zero-shot:", zero_shot(c, t)); print(" few-shot :", few_shot(c, t))
        d, r = multi_pass(c, t); print(" multi-pass review:", r[:200])
