"""Spoke: merges the other spokes' outputs into one study lesson."""
from claude_agent_sdk import AgentDefinition

NAME = "study-synthesizer"

AGENT = AgentDefinition(
    description=(
        "Spoke agent that merges research notes, a worked example, and practice "
        "questions into one coherent study lesson with a cheat sheet and a "
        "self-check list."
    ),
    prompt="""You receive outputs from the other spokes via the hub. Merge them into one lesson. Add no new facts.

## Output format
1. **One-paragraph summary**
2. **Core concepts**: the researcher's points, deduplicated and ordered from simple to advanced.
3. **Worked example**: the example-builder's diagram and walkthrough, unchanged apart from tidying.
4. **Cheat sheet**: a table with columns Pattern | Use when | Avoid when | Exam trap.
5. **Practice questions**: from the question-writer, answers placed at the end.
6. **Self-check**: 5 "can I explain this?" prompts.
7. **Open items**: every UNVERIFIED tag, plus any contradiction between spokes, listed explicitly.

If two spokes disagree, show both versions. Do not pick one silently.""",
    tools=["Read", "Write"],
    disallowedTools=["Agent"],
    model="sonnet",
    maxTurns=10,
    effort="medium",
    permissionMode="default",
    background=False,  # runs last; the hub waits on it
)
