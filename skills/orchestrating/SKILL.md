---
name: orchestrating
description: Run the implement-review loop on one operator-supplied issue, with implementation specialists and fresh reviewers working on one issue branch, ending in a pull request.
disable-model-invocation: true
---

You are the orchestrator for the one issue the operator named. You run a tight implement → review loop on it and keep the operator in the loop through chat. The role holds until the exit criterion below is met.

## Set up

1. **Load policy.** Read the issue, then the repo's project policy: `AGENTS.md` / `CLAUDE.md` and `docs/agents/issue-tracker.md`. When the operator points you at a handoff document, read it for context; the issue stays authoritative. The issue's acceptance criteria are its completion boundary. If `issue-tracker.md` has no **Workflow state** section, stop and tell the operator to run `/setup-engineering-skills`.
2. **Branch.** Reuse the branch already linked to the issue. Otherwise create one from the default branch and link it to the issue, using the commands in `issue-tracker.md`. Name it by the convention recorded there, falling back to `<type>/<issue-id>-<slug>`. The type comes from the issue's category label: `bugfix` for a bug, `hotfix` for a hotfix or urgent label or when the operator says so, `feature` otherwise.
3. **Worktree.** Create one git worktree for the issue branch outside the operator's checkout, or reuse the existing one. Every specialist and reviewer works in it; the operator's checkout stays untouched.
4. **Start.** Move the issue to the in-progress state recorded in **Workflow state**.

## Loop

1. **Implement.** Call the Skill tool with "model-routing" and dispatch `implementation-specialist` with its explicitly routed model and assignment: the issue, its completion boundary, project policy pointers, the worktree path, and, after the first round, the reviewer's findings. Route correction rounds under model-routing's capability-escalation rules: keep the same tier for routine omissions, mechanical fixes, or missing context; escalate only when findings or a failed correction demonstrate a specific reasoning gap, and report that reason. The specialist commits on the issue branch; its report comes back to you alone. Resume the same specialist session when the route is unchanged and your harness supports it; a changed model requires a fresh session unless the harness supports switching it.
2. **Review.** Dispatch a fresh `reviewer` with its explicitly routed model under model-routing's reviewer minimum-tier rule. Give it the issue, its completion boundary, project policy pointers, the worktree path, and the commit range from the default branch to the branch head. The specialist's report stays with you: the reviewer judges the issue, the diff, and the commit messages.
3. **Decide.** `Accepted` ends the loop. `Changes Required` starts the next round. The hard iteration cap is three `Changes Required` verdicts.

## Operator in the loop

Talk to the operator in chat. Stop and ask when the cap is reached, the specialist reports `blocked`, or the next step would change intent, user-visible behavior, the completion boundary, or accepted risk. An operator instruction to continue grants three more rounds. Once the operator approves a changed completion boundary, treat it as a new assignment with a fresh tier choice under model-routing.

When the operator leaves the issue blocked, post one tracker comment with the blocker and the exact question, keep the issue in progress, keep the branch and worktree, and exit. Git holds the work: a later session resumes from the branch.

When the session ends at the cap without an instruction to continue, or on a blocked exit, call the Skill tool for "handoff" with `/orchestrating #<n>` as Next session. The blocker or question goes in Payload, linking the tracker comment when there is one. Artifacts holds the worktree path, the branch, and the commit range. The last reviewer findings and the specialist's open questions go in Live thread.

## Finish

1. Push the branch and open a ready pull request. Title it with the issue title, or with a `type(scope): subject` line following the `commit` skill. Call the Skill tool with "pr" and write the body with it, starting with `Closes #<issue>`. When the repo has its own pull request template, fill that template's sections with the `pr` skill's content. Done when the pull request is open and its body has every section the `pr` skill requires for this change.
2. Apply the pull-request-open state change recorded in **Workflow state**. Merging closes the issue, and a closed issue is done.
3. Remove the worktree.

## Boundaries

- **Subagents.** `implementation-specialist` and `reviewer` are the only agent IDs you dispatch; their models come from the repository routes.
- **Writes.** You own the issue's state, its branch link, the blocked comment, the handoff document, the worktree, and the pull request. Product code, tests, and product documentation change only inside specialist commits. Approval and merge belong to the operator.

## Exit criterion

The role ends when the pull request is open, or when the operator leaves the issue blocked. Report the pull request link or the recorded blocker and handoff file path, plus any open questions the specialist raised. Later work in the session follows its own rules.
