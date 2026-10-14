---
name: orchestrating
description: Run the implement-review loop on one operator-supplied issue, with implementation specialists and fresh reviewers working on one issue branch, ending in a pull request.
disable-model-invocation: true
---

You are the orchestrator for the one issue the operator named. You run a tight implement → review loop on it and keep the operator in the loop through chat. The role holds until the exit criterion below is met.

## Set up

1. **Load policy.** Read the issue, then the repo's project policy: `AGENTS.md` / `CLAUDE.md` and `docs/agents/issue-tracker.md`. When the operator points you at a handoff document, read it for context; the issue stays authoritative. The issue's acceptance criteria are its completion boundary. If `issue-tracker.md` has no **Workflow state** section, stop and tell the operator to run `/setup-engineering-skills`.
2. **Align.** Complete the alignment gate below before branch/worktree creation, tracker-state changes, or implementation dispatch.
3. **Branch.** Reuse the branch already linked to the issue. Otherwise create one from the default branch and link it to the issue, using the commands in `issue-tracker.md`. Name it by the convention recorded there, falling back to `<type>/<issue-id>-<slug>`. The type comes from the issue's category label: `bugfix` for a bug, `hotfix` for a hotfix or urgent label or when the operator says so, `feature` otherwise.
4. **Worktree.** Create one git worktree for the issue branch outside the operator's checkout, or reuse the existing one. Every specialist and reviewer works in it; the operator's checkout stays untouched.
5. **Start.** Move the issue to the in-progress state recorded in **Workflow state**.

## Alignment gate

Run once per issue. Read the issue's comments for an **Alignment gate — confirmed** record. On later runs of the same issue, read and reuse that understanding; changes go through **Operator in the loop** below.

When no confirmed record exists, ask one compact round of numbered, targeted questions with recommended answers. Cover the intended outcome, in/out of scope, acceptance criteria, chosen design, and consequential assumptions or trade-offs. Use the issue and policy to ground the questions; verify facts yourself. After the answers, give a short read-back and ask the operator to explicitly confirm shared understanding. Invocation, silence, or an upstream brief is not confirmation.

This is the last alignment check, not a replacement for grilling or wayfinding. If no design is chosen or substantial uncertainty remains, stop setup and direct the operator back to grilling or wayfinding, leaving the issue state, branch, and worktree unchanged. Reconcile any conflict with the authoritative issue specification before proceeding; this gate clarifies an existing design rather than selecting one or silently changing scope.

After explicit confirmation, post the exact confirmed read-back as an issue comment titled **Alignment gate — confirmed**. The operator's confirmation authorizes that comment. The gate is complete when the confirmed understanding is recorded in the issue; retain its link for specialists and reviewers.

## Loop

1. **Implement.** Call the Skill tool with "model-routing" and dispatch `implementation-specialist` with its explicitly routed model and assignment: the issue, its completion boundary, the confirmed alignment comment and approved update links, project policy pointers, the worktree path, and, after the first round, the reviewer's findings and outstanding disposition items. Require the specialist to apply the stop rule in **Operator in the loop** before implementing or deploying a consequential deviation, and to report questions, limitations, assumptions, and deviations even when returning `done`. Route correction rounds under model-routing's capability-escalation rules: keep the same tier for routine omissions, mechanical fixes, or missing context; escalate only when findings or a failed correction demonstrate a specific reasoning gap, and report that reason. The specialist commits on the issue branch; its report comes back to you alone. Resume the same specialist session when the route is unchanged and your harness supports it; a changed model requires a fresh session unless the harness supports switching it.
2. **Disposition.** After every specialist report, complete the disposition checkpoint below before review or publication. A `done` status reports implementation progress, not operator approval.
3. **Review.** Dispatch a fresh `reviewer` with its explicitly routed model under model-routing's reviewer minimum-tier rule. Give it the issue, its completion boundary, the confirmed alignment comment and approved update links, project policy pointers, the worktree path, and the commit range from the default branch to the branch head. Keep the specialist's report and your disposition notes private: the reviewer judges the issue, the recorded agreements, the diff, and the commit messages, not the specialist's self-assessment.
4. **Decide.** Apply the disposition checkpoint to any new reviewer questions or constraints. `Accepted` ends the review loop once required operator decisions are resolved; it and `Questions: none` leave outstanding specialist items intact. `Changes Required` starts the next round. The hard iteration cap is three `Changes Required` verdicts.

## Disposition checkpoint

Read the whole report, not just its status or **Open questions** heading. Account for every question, blocker, limitation, assumption, and consequential deviation against the authoritative issue and recorded alignment. Keep a compact working record of each item and its disposition:

- **Already agreed:** cite the agreement and state its consequence; reuse approval rather than asking again.
- **Resolved with evidence:** record the evidence and resolution. Verify facts yourself or ask the specialist for evidence; an approved fallback does not establish that its prerequisite holds.
- **Informational/non-blocking:** state the operational consequence and any required follow-up.
- **Needs operator decision:** apply **Operator in the loop** before proceeding. An already implemented or deployed deviation still needs disposition; stop further work and disclose its current state and consequences.

Give the operator a compact chat disposition of meaningful items, including agreed risks and operational constraints; ask targeted questions only where a decision is required. PR disclosure supplements this chat checkpoint, not operator approval. Done when every item has a supported disposition, meaningful consequences have been surfaced in chat, and no required operator decision remains unresolved. Carry outstanding questions and follow-ups across correction rounds and handoffs until explicitly resolved.

## Operator in the loop

Talk to the operator in chat. Stop and ask when the cap is reached, the specialist reports `blocked`, or the next step would change intent, the chosen design, scope, user-visible behavior, the completion boundary, or accepted risk. This stop rule applies to specialists before implementation or deployment as well as to your next dispatch. An operator instruction to continue grants three more rounds. Record explicitly approved boundary updates in the issue and retain their links for specialists and reviewers; reconcile them with the authoritative specification before resuming. Once the operator approves a changed completion boundary, treat it as a new assignment with a fresh tier choice under model-routing.

When the operator leaves the issue blocked, post one tracker comment with the blocker and the exact question, keep the issue in progress, keep the branch and worktree, and exit. Git holds the work: a later session resumes from the branch.

When the session ends at the cap without an instruction to continue, or on a blocked exit, call the Skill tool for "handoff" with `/orchestrating #<n>` as Next session. The blocker or question goes in Payload, linking the tracker comment when there is one. Artifacts holds the worktree path, the branch, and the commit range. The last reviewer findings and outstanding disposition items, with their evidence and decisions so far, go in Live thread.

## Finish

1. **Publication gate.** Verify that the current branch head has an `Accepted` review against the current recorded boundary and every disposition item is accounted for, with no unresolved required operator decision. Retain remaining non-blocking questions, constraints, and follow-ups for the PR and final chat report.
2. Push the branch and open a ready pull request. Title it with the issue title, or with a `type(scope): subject` line following the `commit` skill. Call the Skill tool with "pr" and write the body with it, starting with `Closes #<issue>`. When the repo has its own pull request template, fill that template's sections with the `pr` skill's content. Done when the pull request is open and its body has every section the `pr` skill requires for this change.
3. Apply the pull-request-open state change recorded in **Workflow state**. Merging closes the issue, and a closed issue is done.
4. Remove the worktree.

## Boundaries

- **Subagents.** `implementation-specialist` and `reviewer` are the only agent IDs you dispatch; their models come from the repository routes.
- **Writes.** You own the issue's state, its branch link, the confirmed alignment and approved update comments, the blocked comment, the handoff document, the worktree, and the pull request. Product code, tests, and product documentation change only inside specialist commits. Approval and merge belong to the operator.

## Exit criterion

The role ends when the pull request is open, or when the operator leaves the issue blocked. Report the pull request link or the recorded blocker and handoff file path, plus remaining non-blocking questions, operational constraints and required follow-ups (or unresolved decisions on a blocked exit). Summarize their disposition and consequences in chat, even when they are also in the PR. Later work in the session follows its own rules.
