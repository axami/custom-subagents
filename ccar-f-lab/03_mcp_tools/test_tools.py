"""Model-free tests: error contract + description differentiation."""
import json, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import server

def expect_error(fn, code, **kw):
    try: fn(**kw)
    except ValueError as e:
        p = json.loads(str(e)); assert p["error_code"] == code and "suggestion" in p, p; print(f"PASS {fn.__name__} -> {code}")
    else: raise AssertionError("expected error")

expect_error(server.get_ticket, "INVALID_ID", ticket_id="vpn problem")
expect_error(server.get_ticket, "NOT_FOUND", ticket_id="INC9999")
expect_error(server.search_tickets, "INVALID_ARGUMENT", query="vpn", status="closed")
assert server.get_ticket("INC0012")["host"] == "lnx-vpn-02"; print("PASS get_ticket happy path")
assert len(server.search_tickets("disk")) == 1; print("PASS search happy path")
d1, d2 = server.get_ticket.__doc__, server.search_tickets.__doc__
assert "search_tickets" in d1 and "get_ticket" in d2, "each description must name its sibling"; print("PASS descriptions cross-reference")
