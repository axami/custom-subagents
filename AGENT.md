# Hub-and-Spoke Agent Guidelines

Use this file as the project-level blueprint when creating or updating the CCAR-F study agents. The project is a working example of hub-and-spoke orchestration; keep the agent design consistent with the architecture in `README.md`.

## Architecture

- Create one coordinator as the hub and focused specialist agents as spokes.
- The coordinator owns the user conversation, chooses the topic, delegates work, resolves handoffs, and returns the consolidated result.
- Each spoke has one clearly bounded responsibility and returns its result to the coordinator.
- Spokes never call, message, or delegate to other spokes. All information flows through the coordinator.
- Pass each spoke only the context it needs. Pass source facts and uncertainty labels through unchanged.

## Agent Responsibilities

- `study-coordinator`: route the request and coordinate the workflow; do not replace specialist work with its own explanations.
- `concept-researcher`: research concepts, trade-offs, alternatives, and failure modes using Anthropic documentation and return source URLs.
- `example-builder`: turn supplied research into one concrete, annotated example and show message flow without spoke-to-spoke arrows.
- `exam-question-writer`: create practice questions only from supplied research; never present them as real exam questions.
- `study-synthesizer`: combine the supplied outputs into one lesson without adding unsupported facts or hiding disagreements.

Keep each agent's instructions and tools limited to what its responsibility requires. Give each agent a discoverable name and a description that states its specialty and when to use it.

## Coordination Workflow

1. The coordinator turns the request into a topic, defaulting to hub-and-spoke orchestration when none is specified.
2. It runs `concept-researcher` first.
3. Once the research is available, it runs `example-builder` and `exam-question-writer` in parallel, passing each only the relevant research.
4. It sends the research and both outputs to `study-synthesizer`, which runs last.
5. It returns the synthesized lesson and saves it under `lessons/<topic-slug>.md`.

If a spoke fails, returns incomplete work, or conflicts with another spoke, the coordinator should identify the gap, retry only when useful, and preserve unresolved uncertainty or disagreement in the final lesson.

## Grounding and Output

- Ground research in Anthropic sources. Include URLs for sourced claims.
- Mark claims that could not be confirmed as `UNVERIFIED`; do not invent exam facts or official exam-blueprint details.
- Downstream spokes may reorganize supplied material, but must not introduce new facts.
- Preserve uncertainty labels and disagreements through every handoff and in the final lesson.
- Keep the lesson useful for study: summary, ordered core concepts, worked example, cheat sheet, practice questions with answers, self-check prompts, and open items.

## Adding or Updating an Agent

Before adding a spoke, confirm its responsibility does not duplicate an existing one. Specify its inputs, output format, and grounding limits in its agent file. Update the coordinator's roster and workflow whenever a new spoke changes routing. Keep the README's architecture diagram and usage example accurate when the roster or invocation changes.