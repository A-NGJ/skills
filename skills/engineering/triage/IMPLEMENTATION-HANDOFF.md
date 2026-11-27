# Implementation handoff

Use after the operator selects an issue to implement, either directly during triage or after project prioritization. A ready state alone is not a request to start.

## Preflight

Review the issue body, discussion, tracker links, and relevant repo policy. Verify:

- The authoritative issue body records confirmed scope and testable acceptance criteria for a code PR. Work that requires a shared-environment operation needs a separate assignment or an approved change to the completion boundary.
- Implementation-blocking decisions and dependencies are resolved.
- Necessary execution prerequisites, such as access and tooling, are available.

Use existing triage or other evidence; a readiness label alone does not pass. If a check fails, name the gap and the next action: resolve evaluation or verification gaps through triage, scope or intent gaps with an operator decision, and dependency or prerequisite gaps by unblocking them. If confirmed requirements are missing from the body, get approval for the exact body edit before updating it. Do not repeat full triage when existing evidence suffices. Prepare the handoff only once all checks pass; `orchestrating` still runs its own setup and alignment gates.

## Orchestrator brief

Build the brief from the issue body, comments, and tracker links. It adds no scope and requires no tracker write.

```text
Summary: <one line>
Why now: <priority rationale or operator's explicit selection>
Completion boundary: <link to the issue body's acceptance criteria>
Out of scope: <link to the issue body's scope boundaries, or "not stated">
Dependencies: <blocked-by and blocks links, related issues>
Risks: <known risks and non-blocking questions>
```

Load `handoff` with the issue body link as Payload, the brief in Live thread, and `orchestrating #<n>` as the next assignment. Tell the operator to start `orchestrating` in a fresh session from the resulting document.
