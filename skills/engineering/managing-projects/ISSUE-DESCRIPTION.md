# Issue descriptions

When drafting or rewriting an issue body, use this concise default. Keep repository-required fields and disclaimers.

- Preserve confirmed facts and requirements as established context.
- Describe concrete technical work with enough specificity for a developer to act; match detail to the work.
- Add a worked example between `Scope` and `Acceptance criteria` when prose alone leaves a data shape, grain, calculation, tie-breaker, or state transition easy to misread.
- Add coordination, approvals, open questions, prerequisites, or other sections only when the request or known constraints require them.
- Keep context in Goal, work in Scope, and verifiable outcomes in Acceptance criteria. Omit Related when there are no useful links.

## Worked examples

Include a worked example when an implementer must reason about a non-obvious structure or invariant — such as one logical entity spread across multiple rows or sections, numerator/denominator derivations, deduplication precedence, or an input-to-output transformation where a naive approach fails. Omit it for straightforward work.

- **Walk one concrete instance end-to-end.** Trace a single real record or scenario (using verified identifiers and values from the data, codebase, or issue evidence) across every relevant section, version, or step so the invariant is visible in the numbers. Never invent plausible-looking records; obtain a real one within the read boundary or use an explicitly minimal synthetic case when no data exists yet.
- **Show how the parts reconcile — and the trap.** Demonstrate how counts sum, partition, or transform across the example, and call out the mistake a naive reading would make (for example, why an unweighted average across unequal denominators produces the wrong headline figure, or why same-date reruns cannot be averaged).
- **End with the actionable rule.** Close the example with the exact filter, join, grain, or transition rule the implementation must follow.

```markdown
## Goal

<Short intended outcome and essential established context.>

## Scope

- <Concrete technical work.>

## Acceptance criteria

- [ ] <Observable outcome a developer can verify.>

## Related

<Useful issue or reference links.>
```

The issue body is the authoritative specification. When delegating issue-body writing, including `to-tickets`, retain genuine blocking relationships. Briefs and handoffs link to the body; they carry evidence, decisions, or history rather than a separate set of scope and acceptance criteria. Merge confirmed requirements from older briefs or approved discussion into the body with operator approval; surface conflicts before changing it.
