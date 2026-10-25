"""Run the CCAR-F hub-and-spoke study system with the Claude Agent SDK.

Agent prompts, tools, and models are read from the sibling .md files so they stay the single source of truth.
Usage: python .claude/agents/study_agents.py [topic]
"""
import asyncio
import sys
from pathlib import Path

from claude_agent_sdk import AgentDefinition, ClaudeAgentOptions, ResultMessage, query

AGENTS_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = AGENTS_DIR.parent.parent
HUB = "study-coordinator"
SPOKES = ("concept-researcher", "example-builder", "exam-question-writer", "study-synthesizer")
DEFAULT_TOPIC = "hub-and-spoke orchestration"


def load_agent(name: str) -> tuple[dict[str, str], list[str], str]:
    text = (AGENTS_DIR / f"{name}.md").read_text(encoding="utf-8")
    _, frontmatter, body = text.split("---", 2)
    meta = {}
    for line in frontmatter.strip().splitlines():
        key, value = line.split(":", 1)
        meta[key.strip()] = value.strip()
    tools = [t.strip() for t in meta.get("tools", "").split(",") if t.strip()]
    return meta, tools, body.strip()


def build_spokes() -> dict[str, AgentDefinition]:
    spokes = {}
    for name in SPOKES:
        meta, tools, prompt = load_agent(name)
        spokes[name] = AgentDefinition(
            description=meta["description"],
            prompt=prompt,
            tools=[t for t in tools if t != "Agent"],
            # Spokes never delegate; every handoff goes through the hub.
            disallowedTools=["Agent"],
            model=meta.get("model"),
        )
    return spokes


async def run(topic: str) -> None:
    hub_meta, hub_tools, hub_prompt = load_agent(HUB)
    spokes = build_spokes()
    spoke_tools = {t for spoke in spokes.values() for t in spoke.tools or []}
    (PROJECT_ROOT / "lessons").mkdir(exist_ok=True)

    options = ClaudeAgentOptions(
        system_prompt=hub_prompt,
        model=hub_meta.get("model"),
        allowed_tools=sorted(set(hub_tools) | spoke_tools | {"Agent"}),
        agents=spokes,
        cwd=str(PROJECT_ROOT),
        env={"CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH": "1"},
    )
    async for message in query(prompt=f"Teach me {topic}.", options=options):
        if isinstance(message, ResultMessage):
            print(message.result)


if __name__ == "__main__":
    asyncio.run(run(" ".join(sys.argv[1:]) or DEFAULT_TOPIC))
