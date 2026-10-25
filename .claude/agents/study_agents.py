"""Run the CCAR-F hub-and-spoke study system with the Claude Agent SDK.

Each agent is defined as an AgentDefinition in its own sibling module (AGENT, NAME).
Usage: python .claude/agents/study_agents.py [topic]
"""
import asyncio
import sys
from pathlib import Path

from claude_agent_sdk import AgentDefinition, ClaudeAgentOptions, ResultMessage, query

import concept_researcher
import exam_question_writer
import example_builder
import study_coordinator
import study_synthesizer

AGENTS_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = AGENTS_DIR.parent.parent
HUB = study_coordinator.AGENT
SPOKES = (concept_researcher, example_builder, exam_question_writer, study_synthesizer)
DEFAULT_TOPIC = "hub-and-spoke orchestration"


def build_spokes() -> dict[str, AgentDefinition]:
    return {spoke.NAME: spoke.AGENT for spoke in SPOKES}


async def run(topic: str) -> None:
    spokes = build_spokes()
    spoke_tools = {t for spoke in spokes.values() for t in spoke.tools or []}
    (PROJECT_ROOT / "lessons").mkdir(exist_ok=True)

    options = ClaudeAgentOptions(
        system_prompt=HUB.prompt,
        model=HUB.model,
        allowed_tools=sorted(set(HUB.tools) | spoke_tools | {"Agent"}),
        agents=spokes,
        cwd=str(PROJECT_ROOT),
        env={"CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH": "1"},
    )
    async for message in query(prompt=f"Teach me {topic}.", options=options):
        if isinstance(message, ResultMessage):
            print(message.result)


if __name__ == "__main__":
    asyncio.run(run(" ".join(sys.argv[1:]) or DEFAULT_TOPIC))
