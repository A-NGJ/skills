---
name: handoff
description: Compact the current conversation into a handoff document for another agent to pick up.
argument-hint: "What will the next session be used for?"
metadata:
  upstream:
    repo: "https://github.com/mattpocock/skills"
    author: Matt Pocock
    license: MIT
---

Write a handoff document summarising the current conversation so a fresh agent can continue the work.

## Location

Save to `$TMPDIR/handoff/<skill>-<target>.md`, using the OS temporary directory, never the workspace. `<skill>` is the skill the next session loads and `<target>` is the issue number or a short slug. Overwrite any existing file at that path: the latest handoff for a target is the only one that counts. Writing it needs no confirmation; name the path in chat once it is written.

## Skeleton

```markdown
## Next session
<skill to load> <target>, e.g. `/orchestrating #42`
## Payload
<link to the authoritative issue body; without an issue, the calling skill's payload or a link to its artifact>
## Artifacts
<paths, URLs, branches, worktrees, commit ranges>
## Live thread
<what was in flight and why: decisions, rejected options, operator preferences>
## Suggested skills
<skills the next agent should call the Skill tool for>
```

A calling skill names what goes in Payload and Next session. Called directly, leave Payload out unless the conversation produced one, and take Next session from the arguments.

## Rules

The tracker is the record. A handoff document carries only the between-session context not worth a tracker record. Content already captured in other artifacts (issues, comments, specs, plans, ADRs, commits, diffs) is referenced by path or URL, never copied.

Redact any sensitive information, such as API keys, passwords, or personally identifiable information.

If the user passed arguments, treat them as a description of what the next session will focus on and tailor the doc accordingly.

## Receiving

A session started from a handoff document reads it, then re-reads every tracker record it links before acting. For issue work, the issue body is the specification; comments and the handoff provide context and approval history. If they reveal confirmed requirements missing from or conflicting with the body, pause for an approved body update rather than implementing from the handoff.
