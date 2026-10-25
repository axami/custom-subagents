# CCAR-F Study Project: Agentic Architecture & Orchestration

A hub-and-spoke study system. It is also a working example of the pattern you are learning.

```
                 user
                  |
          study-coordinator (hub)
        /     |        |       \
 concept-   example-  exam-      study-
 researcher builder   question-  synthesizer
                      writer
```

Spokes never talk to each other. The hub passes context and collects results.

## Agents
Each agent is defined twice, with the same settings: a Markdown file for Claude Code and a Python module for the Agent SDK. Edit both together. Both live in `.claude/agents/`.

| Agent | Role | Tools | Turns | Effort | Permission mode |
|---|---|---|---|---|---|
| `study-coordinator` | Hub: picks the topic, delegates, resolves handoffs, saves the lesson | Agent, Read, Write, WebSearch, WebFetch | 30 | high | acceptEdits |
| `concept-researcher` | Spoke: researches concepts from Anthropic docs, returns notes with source URLs | WebSearch, WebFetch, Read | 20 | medium | default |
| `example-builder` | Spoke: builds one annotated worked example with an ASCII diagram | Read | 8 | medium | default |
| `exam-question-writer` | Spoke: writes 6 scenario-based practice questions from the notes | Read | 8 | medium | default |
| `study-synthesizer` | Spoke: merges everything into one lesson with cheat sheet and self-check | Read, Write | 10 | medium | default |

Shared settings: `model: sonnet`, `background: false`. Spokes also set `disallowedTools: Agent`, so they cannot delegate. The hub has `initialPrompt: Teach me hub-and-spoke orchestration.`

Workflow:
1. The hub turns the request into a topic (default: hub-and-spoke orchestration).
2. `concept-researcher` runs first.
3. `example-builder` and `exam-question-writer` run in parallel, each given the research.
4. `study-synthesizer` runs last on all outputs.
5. The hub returns the lesson and saves it to `lessons/<topic-slug>.md`.

Rules for every agent: pass facts through verbatim, keep `UNVERIFIED` tags, show disagreements between spokes instead of picking one, and add no unsupported facts. See `AGENT.md` for the full design guidelines.

### File layout
```
.claude/agents/
  study-coordinator.md   study_coordinator.py
  concept-researcher.md  concept_researcher.py
  example-builder.md     example_builder.py
  exam-question-writer.md exam_question_writer.py
  study-synthesizer.md   study_synthesizer.py
  study_agents.py        runner (Agent SDK)
```
Each `.py` module exposes `NAME` and `AGENT` (an `AgentDefinition`).

## Use
### In Claude Code
Open Claude Code in this folder and ask:

> Use study-coordinator to teach me hub-and-spoke orchestration.

### With the Agent SDK
```
pip install -r requirements.txt
python .claude/agents/study_agents.py "subagent context isolation"
```
With no argument it uses the default topic. `study_agents.py` imports the Python modules and runs the hub with the four spokes as subagents.

Lessons are saved to `lessons/`. Other topics to try: subagent context isolation, parallel vs sequential delegation, handoffs and failure handling.

## Caveat
The agents ground their notes in Anthropic docs and mark anything unconfirmed as UNVERIFIED. They do not know the official exam blueprint, so check the exam guide yourself for the real domain weights.
