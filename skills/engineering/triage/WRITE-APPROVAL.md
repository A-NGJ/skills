# Tracker and repository write approval

Apply these rules within `managing-projects` and `triage`, whether invoked directly or as part of another workflow. Establish the relevant repository policy before writes. Recommendations and read-only investigation do not need write approval. An inherited boundary can narrow permissions; it cannot be widened without operator approval. Any workflow or agent you call inherits the approved boundary.

**Routine tracker administration.** Propose a bounded outcome: affected records, governing policy, permitted operations and their automation effects, exclusions, and an observable exit criterion. Once the operator confirms, handle mechanical details without per-mutation approval. Routine operations can include role or label changes, pointer briefs or requests for information, dependency and duplicate links, placement on an existing project, and other policy-defined maintenance. An operation is not routine if its effect is consequential.

**Consequential changes.** Get explicit approval for the exact changes to closure, rejection, scope, acceptance criteria, priority or milestone commitments, product intent, delivery expectations, or accepted risk. Include every side effect to be applied: label or state changes, closure, tracker comments, and the exact repository edits. For example, approval that a request is out of scope does not by itself authorize writing to `.out-of-scope/` and closing the issue. One confirmation can cover the whole proposed outcome if each consequential change is explicit. Get exact approval for repository edits and any write outside the confirmed boundary before acting.

**Specification edits.** Present the exact proposed body changes for approval. Apply approved description, scope, and acceptance edits to the authoritative issue or PR body and mark it **Edited DD-MM-YY**. Comments may record approval and rationale with a link to the updated body; they never carry a competing specification.

Stop for approval if the actual changes exceed the proposal. This boundary applies to the current request and its delegated work, not to unrelated later assignments.
