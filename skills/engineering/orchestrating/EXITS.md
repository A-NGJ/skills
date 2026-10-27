# Exits without a pull request

## Blocked

When the operator leaves the issue blocked, post one tracker comment with the blocker and the exact question, keep the issue in progress, keep the branch and worktree, delete the scratchpad, and exit.

Recovery is best-effort: Git preserves committed work, not the plan, review status, or unresolved dispositions. A later session reconstructs context from the issue, commits, and any available handoff document; abrupt interruption can lose continuation context, and the branch alone does not establish that it is safe to resume.

## Handoff

When the session ends at the defect-correction budget without an instruction to continue, or on a blocked exit, call the Skill tool for "handoff" with `/orchestrating #<n>` as Next session and `<repo-key>-<issue-id>` as its filename target.

- **Payload:** the blocker or question, linking the tracker comment when there is one.
- **Artifacts:** the worktree path, the branch, the commit range, and the implementation plan with each step's status.
- **Live thread:** the last reviewer findings and outstanding disposition items, with their evidence and decisions so far.

## Local end

When the session ends with neither a pull request nor a block, ask the operator once whether to keep or remove the worktree, and whether to leave the issue in progress or restore its recorded previous state. Removal never forces: keep a dirty worktree and report its path. Delete the scratchpad.
