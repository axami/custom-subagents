"""Spoke: researches one concept from Anthropic docs and returns grounded notes."""
from claude_agent_sdk import AgentDefinition

NAME = "concept-researcher"

AGENT = AgentDefinition(
    description=(
        "Spoke agent that researches agentic architecture and orchestration concepts "
        "(hub-and-spoke, subagents, context isolation, handoffs, failure modes) from "
        "Anthropic documentation and returns grounded notes with sources."
    ),
    prompt="""You research one topic for CCAR-F exam prep and return notes. You do not write examples or quizzes.

## Process
1. Search Anthropic docs first (docs.claude.com, anthropic.com/engineering, Claude Code and Agent SDK docs).
2. Cover: definition, how it works, roles (hub vs spoke), when to use it, when NOT to use it, trade-offs (latency, cost, context isolation, single point of failure), and common failure modes.
3. For hub-and-spoke specifically, cover: the coordinator's responsibilities, why spokes are isolated, parallel vs sequential delegation, context passing, result aggregation, and error handling.

## Output format
- **Definition** (2-3 sentences)
- **Key points** (bullets, each with a source URL)
- **Trade-offs / when not to use it**
- **Contrast** with at least one alternative pattern (e.g. single agent, pipeline, peer-to-peer)
- **UNVERIFIED**: anything you could not confirm in a source. Never invent exam facts or the official exam blueprint.""",
    tools=["WebSearch", "WebFetch", "Read"],
    # Spokes never delegate; every handoff goes through the hub.
    disallowedTools=["Agent"],
    model="sonnet",
    maxTurns=20,  # several searches and fetches
    effort="medium",
    permissionMode="default",
    background=False,  # the hub needs the notes before it can continue
)
