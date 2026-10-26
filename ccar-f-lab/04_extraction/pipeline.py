import sys, json, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from jsonschema import Draft202012Validator
from common.client import get_client, MODEL
from schema import SCHEMA, TOOL, SYSTEM, business_rules
V = Draft202012Validator(SCHEMA); MAX_RETRIES = 2

MOCK = [  # first attempt invalid (bad host pattern + P1 w/o impact), second fixed
 {"stop_reason": "tool_use", "content": [{"type": "tool_use", "id": "a", "name": "record_incident", "input":
   {"host": "LNX_DB_9", "severity": "P1", "symptom": "backup failed", "started_at": None, "customer_impact": False, "confidence": 0.8}}]},
 {"stop_reason": "tool_use", "content": [{"type": "tool_use", "id": "b", "name": "record_incident", "input":
   {"host": None, "severity": "P3", "symptom": "backup failed overnight", "started_at": None, "customer_impact": False, "confidence": 0.8}}]}]

def extract(client, text):
    msgs = [{"role": "user", "content": f"<ticket>{text}</ticket>"}]
    for attempt in range(MAX_RETRIES + 1):
        r = client.messages.create(model=MODEL, max_tokens=800, system=SYSTEM, tools=[TOOL],
                                   tool_choice={"type": "tool", "name": "record_incident"}, messages=msgs)
        call = next(b for b in r.content if b.type == "tool_use")
        data = call.input
        errors = [f"{'/'.join(map(str, e.path)) or '(root)'}: {e.message}" for e in V.iter_errors(data)] + business_rules(data)
        if not errors: return {"status": "ok", "attempts": attempt + 1, "data": data}
        print(f"  attempt {attempt+1} invalid: {errors}")
        msgs += [{"role": "assistant", "content": [{"type": "tool_use", "id": call.id, "name": call.name, "input": data}]},
                 {"role": "user", "content": [{"type": "tool_result", "tool_use_id": call.id, "is_error": True,
                   "content": "Validation failed:\n- " + "\n- ".join(errors) + "\nCall record_incident again with corrected values."}]}]
    return {"status": "needs_human_review", "errors": errors, "data": data}

if __name__ == "__main__":
    client = get_client(MOCK)
    for line in (pathlib.Path(__file__).parent / "data/tickets.jsonl").read_text().splitlines():
        t = json.loads(line); print(t["id"], json.dumps(extract(client, t["text"])))
