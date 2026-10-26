# Tracker integration

Optional issue context, publication, and handoffs for `grill-with-research`.

## Issue input

Read the issue's body, comments, sub-issues, dependencies, and linked branch. Its original purpose bounds the destination; resume from an earlier grill-with-research summary comment when one exists.

## Publication boundary

With an issue, ask once whether the operator authorizes one summary comment and its in-place updates; otherwise treat the issue as read-only context. Pass this boundary to loaded skills.

Creating issues, applying labels, and editing issue bodies belong to `managing-projects` when that integration is chosen.

## Checkpoints

When publication is authorized, maintain one summary comment, created at the first checkpoint and edited in place after that. Link to the authoritative body; record decisions, evidence, and proposed body changes rather than maintaining a second specification. Proposed changes remain pending; they enter the body only through an operator-approved update by `managing-projects` if that integration is chosen.

## Acceptance criteria

For an issue-backed summary, link to the body's criteria and list any proposed edits as pending.

## Handoffs

### Fresh session runs `managing-projects`, if chosen

Use this when the operator wants an issue created or its body reconciled with the confirmed design. Call the Skill tool for "handoff" with the issue body link as Payload and the summary link and pending changes in Live thread; without an issue, link to the chosen summary checkpoint as Payload. Set `/managing-projects <issue-or-slug>` as Next session; it obtains approval for the exact body change before implementation handoff.

### Fresh session runs `orchestrating`, if chosen

Issue only, when the confirmed design agrees with the authoritative body. Call the Skill tool for "handoff" with a link to the issue body as Payload, the local summary path or authorized summary comment link in Live thread, and `/orchestrating #<n>` as Next session. Do not load `orchestrating` in this session. Tell the operator to open a new session, load `orchestrating`, and point it at the file.

## Implementation boundary

When an existing issue governs a build, its body must already contain the confirmed requirements; otherwise offer the `managing-projects` handoff before implementation.
