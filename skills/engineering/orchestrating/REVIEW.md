# Review verdicts that continue the loop

**Reviewer reuse.** Resume the same checkpoint reviewer when its route is unchanged and the harness supports it; otherwise start a fresh reviewer. Every final review, including a re-review after a correction, uses a fresh reviewer.

## Changes Required

The verdict counts toward the defect-correction budget. Start a correction round after any decisions needed for the correction are settled:

1. Dispatch `implementation-specialist` with the findings, resuming the session of the step the findings concern when its route is unchanged and the harness supports it.
2. Route the correction under model-routing's capability-escalation rules: keep the same tier for routine omissions, mechanical fixes, or missing context; escalate only when findings or a failed correction demonstrate a specific reasoning gap, and report that reason.
3. Review again, supplying the updated head SHA, the review range extended through the correction, and the diff since the last reviewed head. The reviewer checks the corrections and possible regressions against the same review boundary.

## Needs clarification

The verdict pauses the protected work and publication. Obtain the missing evidence or resolve the decision through the disposition checkpoint; a code correction needs an established defect, and reviewer uncertainty alone is not one. A question no agreement covers stays unresolved until evidence or a decision settles it.

Request a new verdict only after new evidence or a resolved decision is available, supplying it with the current approved records, head SHA, and review range. A changed final-review head still requires fresh verification.
