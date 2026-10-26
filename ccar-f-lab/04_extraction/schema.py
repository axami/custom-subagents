SCHEMA = {
 "type": "object",
 "properties": {
  "host": {"type": ["string", "null"], "pattern": "^lnx-[a-z0-9-]+$"},
  "severity": {"type": "string", "enum": ["P1", "P2", "P3", "P4"]},
  "symptom": {"type": "string", "maxLength": 200},
  "started_at": {"type": ["string", "null"], "description": "ISO-8601 or null if not stated"},
  "customer_impact": {"type": "boolean"},
  "confidence": {"type": "number", "minimum": 0, "maximum": 1}
 },
 "required": ["host", "severity", "symptom", "started_at", "customer_impact", "confidence"],
 "additionalProperties": False}
TOOL = {"name": "record_incident", "description": "Record the incident fields extracted from the ticket text. Use null when a value is not stated.", "input_schema": SCHEMA}
SYSTEM = ("Extract incident data. Severity: P1 = customer-facing outage; P2 = degraded customer service; "
          "P3 = internal impact only; P4 = no impact/request. Never guess hosts or times — use null.")
def business_rules(d):
    errs = []
    if d.get("severity") == "P1" and not d.get("customer_impact"): errs.append("P1 requires customer_impact=true")
    if d.get("confidence", 1) < 0.5: errs.append("confidence < 0.5: route to human")
    return errs
