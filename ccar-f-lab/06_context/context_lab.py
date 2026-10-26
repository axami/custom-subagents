import json, re, pathlib, random
HERE = pathlib.Path(__file__).parent
random.seed(1)
raw = "\n".join(f"2026-10-26T09:{i%60:02d}:{i%59:02d} {'ERROR' if i%37==0 else 'INFO'} svc=pay pid=4411 "
                f"{'OOM killer invoked' if i%111==0 else 'heartbeat ok'} latency_ms={random.randint(20,900)}" for i in range(2000))
tok = lambda s: len(s) // 4  # rough estimate

def distil(text):
    lines = text.splitlines(); errs = [l for l in lines if " ERROR " in l]
    lat = [int(m) for m in re.findall(r"latency_ms=(\d+)", text)]
    return {"source": "pay.log", "lines": len(lines), "error_count": len(errs),
            "first_error": errs[0][:19] if errs else None, "oom_events": text.count("OOM killer"),
            "latency_p95_ms": sorted(lat)[int(len(lat)*.95)], "raw_path": "logs/pay.log"}

facts = distil(raw)
print(f"raw ≈ {tok(raw):,} tokens  ->  distilled ≈ {tok(json.dumps(facts))} tokens"); print(json.dumps(facts, indent=1))
(HERE / "logs").mkdir(exist_ok=True); (HERE / "logs/pay.log").write_text(raw)

pad = {"task": "Investigate payment latency", "facts": [facts],
       "decisions": ["Not network: LB health OK at 09:10"], "open_questions": ["Heap size on pid 4411?"],
       "next_step": "Delegate heap analysis to subagent; then propose restart in change window"}
(HERE / "scratchpad.json").write_text(json.dumps(pad, indent=1))
print("\n--- new session resumes from scratchpad only ---")
p = json.loads((HERE / "scratchpad.json").read_text())
print(f"Resuming '{p['task']}'. Next: {p['next_step']}. Open: {p['open_questions']}")
