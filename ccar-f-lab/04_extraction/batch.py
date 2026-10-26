"""Message Batches API: submit / status / results. Usage: python batch.py submit|status <id>|results <id>"""
import sys, json, pathlib, anthropic
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common.client import MODEL
from schema import TOOL, SYSTEM
c = anthropic.Anthropic(); cmd = sys.argv[1]
if cmd == "submit":
    reqs = [{"custom_id": t["id"], "params": {"model": MODEL, "max_tokens": 800, "system": SYSTEM, "tools": [TOOL],
             "tool_choice": {"type": "tool", "name": "record_incident"},
             "messages": [{"role": "user", "content": f"<ticket>{t['text']}</ticket>"}]}}
            for t in map(json.loads, (pathlib.Path(__file__).parent / "data/tickets.jsonl").read_text().splitlines())]
    b = c.messages.batches.create(requests=reqs); print("batch id:", b.id, b.processing_status)
elif cmd == "status":
    b = c.messages.batches.retrieve(sys.argv[2]); print(b.processing_status, b.request_counts)
elif cmd == "results":
    for r in c.messages.batches.results(sys.argv[2]):          # order NOT guaranteed -> key by custom_id
        if r.result.type == "succeeded":
            tu = next(x for x in r.result.message.content if x.type == "tool_use"); print(r.custom_id, tu.input)
        else:
            print(r.custom_id, "FAILED:", r.result.type, "-> resubmit just this id")  # errored/expired/canceled
