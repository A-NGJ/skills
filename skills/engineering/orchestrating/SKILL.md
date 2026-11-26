---
name: orchestrating
description: Run the plan-implement-review loop on one operator-supplied issue, with implementation specialists working step by step and fresh reviewers on one issue branch, ending in a pull request.
disable-model-invocation: true
---

You are the orchestrator for the one issue the operator named. You run a tight plan → steps → review loop on it and keep the operator in the loop through chat. The role holds until the exit criterion below is met. Only one orchestrator may be active for an issue; the operator must ensure an earlier session has stopped before resuming. This is an operator-managed precondition, not an enforced lock.

## Set up

1. **Load policy.** Read the issue, then the repo's project policy: `AGENTS.md` / `CLAUDE.md` and `docs/agents/issue-tracker.md`. If `issue-tracker.md` has no **Workflow state** section, stop and tell the operator to run `setup-engineering-skills` using the harness's skill command.
2. **Existing pull request.** Check for an open pull request linked to the issue or using its linked branch. If one exists, report its link and that the exit criterion is already met, then exit without changing the tracker, branch, or worktree. Further changes require an explicit follow-up assignment.
3. **Preflight.** Before writing tracker records or creating a branch or worktree, check both:
   - **Delivery boundary.** The issue body has testable acceptance criteria for a code PR and does not require executing shared-environment operations. Briefs, comments, and handoffs provide context and approval history, not a replacement specification. If confirmed requirements exist only in comments or criteria are missing or untestable, stop and request an approved body update. If criteria require executing a shared-environment operation, stop and propose an approved body update or a separate assignment for the operation.
   - **Integration base.** Resolve the branch this change will merge into from the documented policy, branch/PR commands, and any merge-target restrictions. If policy names no base, use the verified remote default. For a local-only repo without a documented base, ask the operator. Verify the branch exists on the target remote, or locally for a local-only repo. If policy conflicts, the base cannot be resolved, or a linked branch is known to have been created for another base, stop and ask before reusing or changing anything. Retain the resolved base for branch creation, final review, and PR publication.
4. **Align.** On Pi, before writing tracker records or creating a branch or worktree, load `model-routing` and use its Pi reference to confirm that both agent profiles and explicit model and working-directory selection are available. If not, stop and report what's missing. Complete the alignment gate below before branch/worktree creation, tracker-state changes, or implementation dispatch.
5. **Branch.** Reuse the branch already linked to the issue. Otherwise create one from the resolved integration base and link it to the issue, using the commands in `issue-tracker.md`. Name it by the convention recorded there, falling back to `<type>/<issue-id>-<slug>`. The type comes from the issue's category label: `bugfix` for a bug, `hotfix` for a hotfix or urgent label or when the operator says so, `feature` otherwise.
6. **Worktree.** Run `git worktree list` and match the issue id in the branch name, whatever its type or slug. Reuse a single match; with several, stop and ask the operator which to keep. With no match, take the main checkout path from the first entry of `git worktree list --porcelain` and derive `<main-checkout-parent>/<main-checkout-name>-worktrees/<issue-id>` from it, independent of the current directory and branch slug. If the target is occupied (including by an empty directory or a dangling symlink), stop and report the path; do not overwrite it or choose another location. Otherwise, create the issue branch's worktree at that path. Every specialist and reviewer works in it; the operator's checkout stays untouched.
7. **Start.** Derive `<repo-key>` as the SHA-256 hex digest of the normalized remote host and repository path, without credentials or a trailing `.git`; for a local-only repository, hash the canonical main-checkout path instead. Use `<repo-key>-<issue-id>` as the artifact target for both the scratchpad and handoff document. The scratchpad is `orchestrating-<repo-key>-<issue-id>.md` in the harness temp directory, outside the repo and the worktree. It holds the round count, the dispositions, and the issue's previous state, and its path stays with you. If it exists and the issue is in progress, ask the operator whether another session is running; otherwise replace it, keeping only its recorded previous state. Record the issue's current state as the previous state unless it is already in progress or one was kept, then move the issue to the in-progress state recorded in **Workflow state**.

## Alignment gate

Run once per issue. Read the issue's comments for an **Alignment gate — confirmed** record or an upstream confirmed-design record: a grilling, grill-with-research, or triage comment that names the operator's approval of the design. Check an upstream record against the issue's current acceptance criteria; a mismatch counts as no record. On later runs of the same issue, reuse that understanding; changes go through **Operator in the loop**.

With no confirmed record, complete [ALIGNMENT.md](ALIGNMENT.md). The gate is complete when the confirmed understanding is recorded in the issue; when an upstream record is reused, post no second comment. Retain the record's link for specialists and reviewers.

## Dispatch rules

Before every specialist or reviewer dispatch, re-read the round count in the scratchpad and run `git status --porcelain` in the issue worktree; require empty output. If it is dirty, stop and disclose the changes for separate reconciliation before resuming. Never silently commit or discard pre-existing changes. Load `model-routing` before the first dispatch unless its instructions are retained in context, and apply it, with its revalidation rules, before every dispatch.

The **standard assignment** carries the issue, its completion boundary, the confirmed alignment record and approved update links, project policy pointers including `docs/agents/verification.md` when it exists, and the worktree path. A specialist also gets the outstanding disposition items.

A **consequential change** alters intent, the chosen design, scope, user-visible behavior, the completion boundary, or accepted risk. Before one, a specialist makes no change for it, commits only the safe work, and returns `blocked` with the exact question. It reports minor deviations, limitations, assumptions, and questions even when returning `done`. Its report comes back to you alone.

## Plan

1. **Plan.** When the confirmed alignment record already has ordered steps, use them as the plan and skip the dispatch. When it describes a single step with no operational step, skip the dispatch and show a one-line plan. Otherwise dispatch `implementation-specialist` in plan mode with the standard assignment. It returns an implementation plan: each acceptance criterion mapped to the current state and the gap, ordered steps, operational steps, consequential choices, a risky tag on each step that changes shared infrastructure, a schema or migration, a public interface, or security-sensitive code, and any proposed checkpoints under **Steps**. Risky tags set the review tier, not the checkpoint cadence.
2. **Check the plan.** Done when every acceptance criterion maps to a step or to an open question, every shared-environment operational step (deploy, migration, backfill, manual action) is recorded as a follow-up for a later assignment rather than an executable step, each executable step is small enough for one focused session, the risky tags are correct, and each proposed checkpoint names the downstream implementation work it protects, why waiting would materially amplify a mistake, and the completed obligations and relevant invariants to review; when the plan dispatch was skipped, make these checks yourself. A requirement the plan exposes — a gap the issue implies but the alignment record does not settle — goes through the disposition checkpoint now, before any code exists. Return the plan for revision when a check fails; a single step is a valid plan for a small issue.
3. **Show.** Post the plan compactly in chat; when the plan dispatch was skipped, list each step's risky tag with a one-line reason. Ask only for decisions the disposition checkpoint marks **Needs operator decision**; otherwise proceed.

## Steps

Run the plan's executable steps (implementation and local or disposable-environment verification) in order, all on the issue branch in the one worktree.

1. **Implement.** Dispatch a fresh `implementation-specialist` session for the step, with a fresh tier choice for that step's difficulty. Add to the standard assignment: the implementation plan, this step's scope and checks, and the commits of earlier steps. The specialist commits only this step's work.
2. **Disposition.** After every specialist report, complete the disposition checkpoint below. A `done` status reports step progress, not operator approval. When a step reveals that the plan is wrong, revise the remaining steps and show the change in chat; consequential changes go through **Operator in the loop**.
3. **Checkpoint review.** Run **Review** only when the plan records concrete downstream implementation work that would materially amplify a mistake. Review the prerequisite commits before the protected work begins, against the recorded completed obligations and relevant invariants. Otherwise defer to final review; when no protected work remains, final review replaces the checkpoint.

## Review

1. **Start review.** Dispatch a fresh `reviewer` at each checkpoint and, after the last step, at final review. Apply model-routing's reviewer tier floor, at `standard` or higher when the commit range contains a risky-tagged step. Supply the review type (checkpoint or final), the standard assignment, the head SHA, and the commit range: prerequisite commits for a checkpoint, the merge base with the resolved integration branch to branch head for final review. A checkpoint also gets its recorded completed obligations and relevant invariants as its review boundary; unfinished issue requirements remain context, not checkpoint acceptance criteria. The reviewer judges the issue, the recorded agreements, the diff, and the commit messages, so it gets nothing from the implementation plan, the specialist reports, or your scratchpad. Tell it that `Changes Required` is for established defects, and `Needs clarification` is for missing evidence or an unsettled decision that prevents a verdict, including uncertainty about an intentional deviation, limitation, or assumption.
2. **Decide.** Apply the disposition checkpoint to any new reviewer questions or constraints, and verify that the agreement you cite for a question actually covers it. `Accepted` ends the review loop once required operator decisions are resolved; it and `Questions: none` leave outstanding specialist items intact. For `Changes Required` or `Needs clarification`, follow [REVIEW.md](REVIEW.md).

The defect-correction budget is three `Changes Required` verdicts per session, counting checkpoint and final reviews together; keep the count in the scratchpad. Planning revisions, clarification attempts, and other follow-ups do not count. This is not an overall effort or iteration cap; stop at the defect budget unless the operator explicitly instructs you to continue.

## Disposition checkpoint

Read the whole report, not just its status or **Open questions** heading. Account for every question, blocker, limitation, assumption, and consequential deviation against the authoritative issue and recorded alignment. Keep a compact working record in the scratchpad of each item and its disposition:

- **Covered:** quote the exact sentence of the agreement or record the evidence, and state its consequence; reuse approval rather than asking again. Verify facts yourself or ask the specialist for evidence; an approved fallback does not establish that its prerequisite holds.
- **Needs operator decision:** apply **Operator in the loop** before proceeding. An already implemented or deployed deviation still needs disposition; stop further work and disclose its current state and consequences.

Give the operator a compact chat disposition of meaningful items, including agreed risks and operational constraints, with informational items in one line; ask targeted questions only where a decision is required. PR disclosure supplements this chat checkpoint, not operator approval. Done when every item has a supported disposition, meaningful consequences have been surfaced in chat, and no required operator decision remains unresolved. Carry outstanding questions and follow-ups across correction rounds and handoffs until explicitly resolved.

## Operator in the loop

Talk to the operator in chat. Stop and ask when the defect-correction budget is reached, the specialist reports `blocked`, or the next step would be a consequential change. An operator instruction to continue adds three rounds; state the running `Changes Required` total when asking.

Get explicit approval for every consequential change. When it changes the specification, present the exact issue-body edit for approval and apply it to the authoritative body before resuming. Record every approved consequential change in an issue comment, whether or not the body changes: state the approved decision, rationale, consequences, and any superseded agreement, linking to the body when it was updated. Retain the comment link for specialists and reviewers. Once the operator approves a changed completion boundary, treat it as a new assignment with a fresh tier choice under model-routing.

When the operator leaves the issue blocked, the session ends at the defect-correction budget, or it ends locally with neither a pull request nor a block, follow [EXITS.md](EXITS.md).

## Finish

1. **Publication gate.** Verify that the current branch head has an `Accepted` final review against the issue's complete current recorded boundary and every disposition item is accounted for, with no unresolved required operator decision. Retain remaining non-blocking questions, constraints, and follow-ups for the PR and final chat report.
2. Push the branch and open a ready pull request targeting the resolved integration base. Title it with the issue title, or with a `type(scope): subject` line following the `commit` skill. Load `pr` and write the body with it, starting with `Closes #<issue>`. When the repo has its own pull request template, fill that template's sections with the `pr` skill's content. Done when the pull request is open and its body has every section the `pr` skill requires for this change.
3. Apply the pull-request-open state change recorded in **Workflow state**. If merging into the integration base will not auto-close the issue, report that the operator must close it after merge.
4. Keep the worktree until the pull request merges and report its path in the final chat message. Delete the scratchpad.

## Boundaries

- **Subagents.** `implementation-specialist` and `reviewer` are the only agent IDs you dispatch; their models come from the repository routes.
- **Operations.** This assignment produces a pull request, not a deployment. Specialists may prepare operational code and documentation and verify them locally or in disposable environments; deployments, migrations, backfills, and other shared-environment mutations belong to explicit follow-up assignments, even when the design is approved.
- **Writes.** You own the issue's state, its branch link, explicitly approved specification edits to its body, the confirmed alignment and approved update comments, the blocked comment, the handoff document, the scratchpad, the worktree and its removal, and the pull request. Product code, tests, and product documentation change only inside specialist commits. Approval and merge belong to the operator.

## Exit criterion

The role ends when the pull request is open (including an existing one found during setup), when the operator leaves the issue blocked, when the defect-correction budget ends the session, or when the session ends locally with neither a pull request nor a block. Report the pull request link or the recorded blocker and handoff file path, plus remaining non-blocking questions, operational constraints and required follow-ups (or unresolved decisions on a blocked exit). Summarize their disposition and consequences in chat, even when they are also in the PR. Later work in the session follows its own rules.
