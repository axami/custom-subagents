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

## Use
Open Claude Code in this folder and ask:

> Use study-coordinator to teach me hub-and-spoke orchestration.

Lessons are saved to `lessons/`. Other topics to try: subagent context isolation, parallel vs sequential delegation, handoffs and failure handling.

## Caveat
The agents ground their notes in Anthropic docs and mark anything unconfirmed as UNVERIFIED. They do not know the official exam blueprint, so check the exam guide yourself for the real domain weights.
