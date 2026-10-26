# 05 — Prompt Engineering
## Concepts
- **Few-shot for ambiguity**: pick examples at the *decision boundary* (cases that look alike but differ),
  show reasoning briefly, vary format/order so the model doesn't copy surface features. 3-5 diverse > 10 similar.
- **Explicit review criteria**: replace "review this well" with a numbered rubric + severity definitions +
  required output format. Criteria make results consistent and auditable.
- **Multi-pass architecture**: generate → critique against criteria (separate call, fresh context) → revise.
  Or split: classify → route → specialist prompt. Independent reviewer avoids self-confirmation bias.
- Structure with XML tags (`<ticket>`, `<examples>`), put long docs first and the question last, give role in system prompt.
## Steps
`python prompts.py --offline` then live. Compare `zero_shot` vs `few_shot` on the AMBIGUOUS set; then run `multi_pass`.
## Exam traps
- Inconsistent outputs → add examples/criteria, not "temperature 0" alone.
- Self-review in the same context is weaker than an independent pass.
