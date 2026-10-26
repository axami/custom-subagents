"""SupportOps MCP server: two deliberately similar tools, differentiated by description + structured errors."""
import re, json
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("supportops")
TICKETS = {"INC0012": {"id": "INC0012", "title": "VPN drops every 30 min", "status": "open", "host": "lnx-vpn-02"},
           "INC0013": {"id": "INC0013", "title": "Disk full /var/log", "status": "resolved", "host": "lnx-web-07"}}

def err(code, message, retryable=False, suggestion=None):
    # FastMCP marks raised exceptions as isError=true; we raise with a JSON payload for structure.
    raise ValueError(json.dumps({"error_code": code, "message": message, "retryable": retryable, "suggestion": suggestion}))

@mcp.tool()
def get_ticket(ticket_id: str) -> dict:
    """Fetch ONE ticket by its exact ID (format INC + 4-7 digits, e.g. INC0012).
    Use ONLY when you already know the ID. If you only have keywords or symptoms, use search_tickets instead.
    Returns: id, title, status, host."""
    if not re.fullmatch(r"INC\d{4,7}", ticket_id):
        err("INVALID_ID", f"'{ticket_id}' is not a ticket ID.", suggestion="Use search_tickets with keywords to find the ID.")
    if ticket_id not in TICKETS:
        err("NOT_FOUND", f"{ticket_id} does not exist.", suggestion="Check the ID or use search_tickets.")
    return TICKETS[ticket_id]

@mcp.tool()
def search_tickets(query: str, status: str = "any", limit: int = 5) -> list[dict]:
    """Full-text search across ticket titles when the ticket ID is UNKNOWN (e.g. 'VPN', 'disk full').
    status: 'open' | 'resolved' | 'any'. Returns up to `limit` (1-20) summaries; call get_ticket for full detail.
    Do NOT use this to look up a known ID."""
    if status not in ("open", "resolved", "any"):
        err("INVALID_ARGUMENT", f"status '{status}' invalid", suggestion="Use open, resolved or any.")
    if not 1 <= limit <= 20:
        err("INVALID_ARGUMENT", "limit must be 1-20", suggestion="Use limit=5.")
    hits = [t for t in TICKETS.values() if query.lower() in t["title"].lower() and status in ("any", t["status"])]
    return hits[:limit]

@mcp.resource("runbook://{name}")
def runbook(name: str) -> str:
    """Read-only runbook text attached by the client app."""
    return {"disk-full": "1. du -xh /var/log | sort -h  2. check logrotate  3. escalate if >95% after rotate"}.get(name, "not found")

if __name__ == "__main__":
    mcp.run()  # stdio
