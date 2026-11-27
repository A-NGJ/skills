# Issue descriptions

The issue body is the authoritative specification. See [External PR](#external-pr) for where to specify remaining PR work. Follow repository requirements and templates first. Use the compact default below otherwise; preserve required fields and disclaimers.

- **Goal:** State the intended outcome and essential established context. Use the [guidance by kind](#guidance-and-examples-by-kind) to decide which details matter.
- **Scope:** Describe the concrete technical work in terms of durable behavior and contracts. Give a developer enough detail to act, scaled to the work. Name interfaces, types, or config shapes when they clarify the contract; avoid file paths, line numbers, and procedural steps that will go stale or prescribe an unapproved design.
- **Acceptance criteria:** State observable outcomes a developer can verify independently. Include relevant edge cases and failure behavior.
- **Optional sections:** Add **Out of scope** when an adjacent change might look included. Add a [worked example](#worked-examples) when prose alone leaves an invariant easy to misread. Add prerequisites, open questions, coordination, or approvals only when the request or known constraints require them. Omit **Related** when there are no useful links. Preserve genuine blocking relationships when drafting or delegating issue writing, including through `to-tickets`.

Reconcile prior briefs and discussion with the body. Preserve confirmed facts and requirements; surface conflicts and unapproved scope before updating it. Merge confirmed requirements into the body only after approval of the exact edit. Briefs and handoffs link to the body and carry evidence, decisions, or history rather than a second specification.

## Default template

```markdown
## Goal

<Short intended outcome and essential established context.>

## Scope

- <Concrete technical work.>

## Acceptance criteria

- [ ] <Observable outcome a developer can verify.>

## Related

<Useful issue or reference links; omit this section if there are none.>
```

## Guidance and examples by kind

Use the same template for each kind. The examples below are illustrative drafts.

### Bug

Record the conditions and steps needed to reproduce the problem, and distinguish observed behavior from expected behavior. Make the acceptance criteria check the original failure and the behavior that should stay unchanged.

```markdown
## Goal

Skill descriptions should remain readable when shortened. Load a skill whose
`description` is `word ` repeated 204 times followed by `boundary`. The
1,024-character cutoff displays only `boun` of the final word.

## Scope

- Shorten over-limit descriptions at a word boundary when one fits, reserving
  space for `...` within the existing limit.

## Acceptance criteria

- [ ] A description of exactly 1,024 characters is unchanged.
- [ ] In the reported case, the result keeps all 204 complete words, ends in
      `word...`, and is at most 1,024 characters.
```

### Enhancement

Name who needs the improvement and why, what the current behavior prevents or makes harder, and what they should be able to do after the change.

```markdown
## Goal

Maintainers need to recover why a feature was declined when someone requests it
again. Today the reason is only in the closed issue's discussion.

## Scope

- Keep a concept-based record of each rejected enhancement in `.out-of-scope/`
  so triage can surface the prior decision for a similar request.

## Acceptance criteria

- [ ] Rejecting an enhancement creates or updates a record with the decision,
      its rationale, and a link to the issue.
- [ ] Triaging the same request under different wording surfaces the prior record.
- [ ] Closing a bug does not create a rejection record.
```

### External PR

Describe what the diff already delivers, what remains to be finished or corrected, and what behavior must stay unchanged. Put these requirements in the governing issue body when one exists; otherwise put them in the PR body, as in the example below.

```markdown
## Goal

The PR adds `triage list --json`, and successful runs already emit JSON.
Errors still emit human-readable text, so scripts cannot parse failed runs
using the same format.

## Scope

- Finish the JSON error path without changing the existing success payload,
  exit codes, or output when `--json` is absent.

## Acceptance criteria

- [ ] Successful runs with `--json` still emit the existing JSON payload.
- [ ] With the tracker unavailable, `--json` emits `{"error":"<message>"}` on
      stdout and retains the existing nonzero exit code.
- [ ] Without `--json`, success and failure output and exit codes are unchanged.
```

## Worked examples

Add a worked example between Scope and Acceptance criteria when an implementer must reason about a non-obvious data shape, grain, calculation, state transition, tie-breaker, or other invariant. Examples include one logical entity spread across multiple rows or sections, a derived numerator and denominator, deduplication precedence, or an input-to-output transformation a naive approach would get wrong. Omit it for straightforward work.

- **Walk one concrete instance end to end.** Within the approved read boundary, choose one real record or scenario with verified identifiers and values from the data, codebase, or issue evidence. Trace it across every relevant section, version, or step so the invariant is visible. Never invent plausible-looking records; use a clearly labeled minimal synthetic case when no real data exists yet.
- **Show how the parts reconcile and identify the trap.** Demonstrate how counts sum, partition, or transform, and explain the tempting mistake: for example, why an unweighted average across unequal denominators gives the wrong headline figure, or why averaging same-date reruns is wrong when only one version should count.
- **End with the actionable rule.** State the exact filter, join, grain, tie-breaker, or transition the implementation must honor.
