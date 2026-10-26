"""Module 01: hand-built agentic loop with tool calling, error handling, subagents, sessions."""
import sys, os, json, time, uuid, random, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common.client import get_client, MODEL, OFFLINE, text_of

MAX_TURNS = int(os.getenv("MAX_TURNS", 10))
SESS_DIR = pathlib.Path(__file__).parent / "sessions"; SESS_DIR.mkdir(exist_ok=True)

# ---------- tools (fake infra) ----------
def get_metrics(host: str):
    if not host.startswith("lnx-"):
        raise ValueError(f"Unknown host '{host}'. Hosts must start with 'lnx-'.")
    return {"host": host, "cpu_pct": 93, "load_1m": 11.2, "mem_pct": 71, "top_proc": "java (pid 4411)"}
def get_disk(host: str):
    return {"host": host, "/": "62%", "/var/log": "97%"}
def delegate_log_analysis(host: str, question: str):
    return run_subagent(host, question)

TOOLS = [
 {"name": "get_metrics", "description": "Return live CPU, load, memory and top process for ONE Linux host. "
  "Use first when a host is reported slow. Does NOT return disk usage (use get_disk).",
  "input_schema": {"type": "object", "properties": {"host": {"type": "string", "description": "e.g. lnx-web-07"}}, "required": ["host"]}},
 {"name": "get_disk", "description": "Return filesystem usage per mount for ONE host. Use for disk-full or I/O symptoms.",
  "input_schema": {"type": "object", "properties": {"host": {"type": "string"}}, "required": ["host"]}},
 {"name": "delegate_log_analysis", "description": "Spawn a log-analysis subagent for verbose log review. Returns a short summary only.",
  "input_schema": {"type": "object", "properties": {"host": {"type": "string"}, "question": {"type": "string"}}, "required": ["host", "question"]}},
]
IMPL = {"get_metrics": get_metrics, "get_disk": get_disk, "delegate_log_analysis": delegate_log_analysis}
SYSTEM = ("You are an L1 CloudOps agent. Investigate with tools, then give: Finding, Evidence, Recommended action. "
          "If a tool errors, read the message and correct your input; do not invent data.")

# ---------- API call with retry ----------
def call(client, **kw):
    for attempt in range(5):
        try:
            return client.messages.create(**kw)
        except Exception as e:
            status = getattr(e, "status_code", None)
            if status in (429, 500, 502, 503, 529) and attempt < 4:
                wait = (2 ** attempt) + random.random(); print(f"  retry {attempt+1} in {wait:.1f}s ({status})"); time.sleep(wait); continue
            raise  # 400/401/403 etc: not retryable

# ---------- tool execution -> tool_result blocks ----------
def run_tools(resp):
    results = []
    for b in resp.content:
        if b.type != "tool_use": continue
        print(f"  -> tool {b.name}({b.input})")
        try:
            out = IMPL[b.name](**b.input)
            results.append({"type": "tool_result", "tool_use_id": b.id, "content": json.dumps(out)})
        except Exception as e:
            results.append({"type": "tool_result", "tool_use_id": b.id, "is_error": True,
                            "content": json.dumps({"error_type": type(e).__name__, "message": str(e), "retryable": False})})
    return results  # ALL results go into ONE user message

# ---------- subagent ----------
def run_subagent(host, question):
    client = get_client([{"stop_reason": "end_turn", "content": [{"type": "text",
        "text": "Summary: OutOfMemory-style GC thrash in java pid 4411 since 09:12; /var/log filling from app.log (no rotation)."}]}])
    logs = "\n".join(f"2026-10-26T09:{m:02d} WARN GC overhead limit approaching pid=4411" for m in range(12, 40))
    r = call(client, model=MODEL, max_tokens=400,
             system="You are a log-analysis subagent. Return <=3 sentences: root-cause hypothesis + evidence timestamps.",
             messages=[{"role": "user", "content": f"Host {host}. Question: {question}\nLOGS:\n{logs}"}])
    return {"summary": text_of(r)}  # parent never sees raw logs

# ---------- sessions ----------
def save(sid, msgs): (SESS_DIR / f"{sid}.json").write_text(json.dumps(msgs, default=lambda o: o.__dict__, indent=1))
def load(sid): return json.loads((SESS_DIR / f"{sid}.json").read_text())
def serialise(content):
    return [{k: v for k, v in b.__dict__.items()} if hasattr(b, "__dict__") else b.model_dump() for b in content] \
        if OFFLINE else [b.model_dump() for b in content]

MOCK = [
 {"stop_reason": "tool_use", "content": [{"type": "text", "text": "Checking metrics and disk in parallel."},
   {"type": "tool_use", "id": "t1", "name": "get_metrics", "input": {"host": "web-07"}},
   {"type": "tool_use", "id": "t2", "name": "get_disk", "input": {"host": "lnx-web-07"}}]},
 {"stop_reason": "tool_use", "content": [{"type": "tool_use", "id": "t3", "name": "get_metrics", "input": {"host": "lnx-web-07"}},
   {"type": "tool_use", "id": "t4", "name": "delegate_log_analysis", "input": {"host": "lnx-web-07", "question": "why is java hot?"}}]},
 {"stop_reason": "end_turn", "content": [{"type": "text", "text": "Finding: java pid 4411 GC thrash + /var/log 97%.\nEvidence: cpu 93%, subagent summary.\nAction: rotate app.log, raise heap / restart in change window."}]},
]

def main():
    args = [a for a in sys.argv[1:] if a != "--offline"]
    sid, msgs = None, []
    if args and args[0] == "--resume": sid, msgs, args = args[1], load(args[1]), args[2:]
    sid = sid or uuid.uuid4().hex[:8]
    msgs.append({"role": "user", "content": " ".join(args) or "Server lnx-web-07 is slow, investigate"})
    client = get_client(MOCK)
    for turn in range(MAX_TURNS):
        resp = call(client, model=MODEL, max_tokens=1500, system=SYSTEM, tools=TOOLS, messages=msgs)
        msgs.append({"role": "assistant", "content": serialise(resp.content)})
        print(f"[turn {turn}] stop_reason={resp.stop_reason}")
        if resp.stop_reason == "tool_use":
            msgs.append({"role": "user", "content": run_tools(resp)})
        elif resp.stop_reason == "max_tokens":
            msgs.append({"role": "user", "content": "Continue from where you stopped."})
        else:  # end_turn / stop_sequence / refusal
            print("\n" + text_of(resp)); break
        save(sid, msgs)
    else:
        print("!! MAX_TURNS reached — stopping to avoid runaway loop (escalate to human).")
    save(sid, msgs); print(f"\nsession: {sid}  (resume with --resume {sid})")

if __name__ == "__main__": main()
