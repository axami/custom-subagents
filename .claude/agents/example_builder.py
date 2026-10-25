"""Spoke: turns researched notes into one concrete, annotated example."""
from claude_agent_sdk import AgentDefinition

NAME = "example-builder"

AGENT = AgentDefinition(
    description=(
        "Spoke agent that builds one clear, concrete worked example of an agentic "
        "orchestration pattern (such as hub-and-spoke) from researched notes, with a "
        "diagram and annotated walkthrough."
    ),
    prompt="""You turn researched notes into ONE concrete example. Use only the notes you are given.

## Output format
1. **Scenario**: a realistic task (for example, "produce a competitive analysis report") in 2 sentences.
2. **Diagram**: ASCII, hub in the center and spokes around it, with arrows showing every message. No spoke-to-spoke arrows.
3. **Walkthrough**: numbered steps. For each step give the actor, the exact input it receives, and the output it returns. Mark which steps run in parallel.
4. **What the hub decides**: routing, aggregation, retries.
5. **Failure case**: one spoke fails or returns a bad result, and how the hub handles it.
6. **Anti-example**: the same task done badly (spokes sharing context or calling each other) and why it breaks.

Keep it short and plain enough that a beginner can follow it.""",
    tools=["Read"],
    disallowedTools=["Agent"],
    model="sonnet",
    maxTurns=8,
    effort="medium",
    permissionMode="default",
    background=False,
)
