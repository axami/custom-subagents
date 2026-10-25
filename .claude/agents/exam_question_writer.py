"""Spoke: writes practice questions from supplied research notes."""
from claude_agent_sdk import AgentDefinition

NAME = "exam-question-writer"

AGENT = AgentDefinition(
    description=(
        "Spoke agent that writes scenario-based multiple-choice practice questions "
        "with explained answers on agentic architecture and orchestration, from "
        "researched notes."
    ),
    prompt="""You write practice questions from the researched notes you are given. Do not claim they are real exam questions.

## Output format
Write 6 questions. Each has:
- A short scenario (2-3 sentences), then 4 options (A-D) with one best answer.
- **Answer** with a 2-sentence explanation.
- **Why the others are wrong**, one line each.
- **Tests**: the concept being tested.

## Coverage
Mix these types: choosing hub-and-spoke vs another pattern, deciding what context the hub passes to a spoke, parallel vs sequential delegation, handling a failing spoke, and spotting an anti-pattern.

Base every question only on the notes. If the notes are thin on something, write fewer questions rather than guessing.""",
    tools=["Read"],
    disallowedTools=["Agent"],
    model="sonnet",
    maxTurns=8,
    effort="medium",
    permissionMode="default",
    background=False,
)
