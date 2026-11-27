# Issue descriptions

The issue body is the authoritative specification. For an external PR, specify the remaining work in its governing issue body, or in the PR body if there is no governing issue. Follow repository requirements and templates first. Use the compact default below otherwise; preserve required fields and disclaimers.

- **Goal:** State the intended outcome and essential established context. Explain current versus desired behavior when the difference matters, especially for bugs or work remaining on a PR.
- **Scope:** Describe what must change in terms of durable behavior and contracts. Name interfaces, types, or config shapes when they clarify the contract; avoid file paths, line numbers, and procedural steps that will go stale or prescribe an unapproved design.
- **Acceptance criteria:** State observable outcomes a developer can verify independently. Include relevant edge cases and failure behavior.
- **Optional sections:** Add **Out of scope** when an adjacent change might look included, **Worked example** when prose can be misread, and prerequisites, open questions, coordination, or **Related** links only when useful. Preserve actual blocking relationships when drafting or delegating issue writing.

Reconcile prior briefs and discussion with the body. Preserve confirmed facts and requirements; surface conflicts and unapproved scope before updating it. Merge confirmed requirements into the body only after approval of the exact edit. Briefs and handoffs link to the body and carry evidence, decisions, or history rather than a second specification.

## Default template

```markdown
## Goal

<Short intended outcome and essential established context.>

## Scope

- <Concrete technical work.>

## Acceptance criteria

- [ ] <Observable outcome a developer can verify.>
```

## Worked examples

Add a worked example between Scope and Acceptance criteria when an implementer must reason about a non-obvious data shape, grain, calculation, state transition, tie-breaker, or other invariant. Omit it for straightforward work.

- **Walk one concrete instance end to end.** Trace a real record or scenario using verified identifiers and values from the data, codebase, or issue evidence. Never invent plausible-looking records; use a clearly labeled minimal synthetic case when no real data exists yet.
- **Show how the parts reconcile and identify the trap.** Show how the rows or counts transform or partition, and explain the tempting mistake (for example, equally weighting averages with unequal denominators).
- **End with the actionable rule.** State the exact filter, join, grain, tie-breaker, or transition the implementation must honor.
