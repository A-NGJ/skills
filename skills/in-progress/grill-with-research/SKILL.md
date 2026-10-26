---
name: grill-with-research
description: Converge a foggy idea or issue into one fixed-scope work item through grilling, research, and prototypes. Works standalone, ending in a converged summary; tracker integrations are optional.
disable-model-invocation: true
---

`grill-with-research` turns a foggy idea into one **fixed-scope work item**: a destination, the decisions that pin it, and testable acceptance criteria someone can later pick up and build. The interview and summary need no repository policy, tracker setup, or issue. You converge through grilling, research, and prototypes within the session. Tracker publication and collaboration with `managing-projects` or `orchestrating` are optional; creating issues, applying labels, and editing issue bodies belong to `managing-projects` when that integration is chosen.

## Start

1. **Load the input.** For an issue, read its body, comments, sub-issues, dependencies, and linked branch; its original purpose bounds the destination, and an earlier grill-with-research summary comment is where you resume. For a handoff document or a pasted summary, resume from its open questions and fog. Otherwise take the loose idea as stated.
2. **Choose the record.** Use local checkpoints by default. With an issue, ask once whether the operator authorizes one summary comment and its in-place updates; otherwise treat the issue as read-only context. Pass this boundary to loaded skills.
3. **Name the provisional destination.** Call the Skill tool for "grilling" and "domain-modeling". Without an agreed glossary or ADR destination, capture vocabulary and decisions in the summary. The first round establishes the desired outcome and constraints; the destination stays provisional while evidence-dependent decisions remain open.
4. **Draft candidate research.** Tie each research question to the decision it informs and the facts needed to settle it.

## Converge

Run grilling rounds until the frontier is empty. Within the rounds:

- **Read back** each ambiguous or garbled answer: state your interpretation and have the operator confirm it in the next round before anything builds on it.
- **Research.** Resolve straightforward facts directly through read-only inspection. For substantive investigations requiring delegated legwork, call the Skill tool for "research"; its approval of the question list is a question in the current round. Gather the findings before asking the operator to choose an option that depends on them; continue independent frontier questions while research is pending. Findings land in chat and shape the next round. When evidence invalidates an assumption, reopen the affected decision and any decisions that depended on it.
- **Prototype.** Use concrete scenarios for questions answerable in prose. When running or seeing something can resolve a named uncertainty, identify the question and the decision it will settle, then call the Skill tool for "prototype". The call is exploration-only: capture validated decisions in the summary; the prototype skill's production-integration step waits for a separately authorized build. Choose isolation before building: repository-dependent prototypes use a separate worktree on a throwaway `prototype/<slug>` branch; standalone demos use the scratchpad. Keep the operator's checkout untouched. Build the smallest prototype that answers the question within the round, and have the operator pick in the next. Commit repository-dependent prototypes on that branch. Record the question, verdict, and branch or standalone artifact path under Evidence.
- **Scope.** When the idea holds several work items, narrow to one and record the rest as follow-ups.
- **Blocked on someone else.** Work only another person can do goes under Blocked on, with a precise checklist for them.

After about six rounds, offer to pause with a progress summary; the operator may continue.

## Checkpoint

Write the running summary before dispatching research or a prototype, after a session compaction, and at session end:

- **Local:** call the Skill tool for "handoff" with the running summary as Payload and `/grill-with-research <issue-or-slug>` as Next session. The temp directory may lose it; for a lasting record, save the summary at an operator-chosen path and use a link to that record as Payload. A durable summary needs no issue.
- **Issue publication, when authorized:** maintain one summary comment, created at the first checkpoint and edited in place after that. Link to the authoritative body; record decisions, evidence, and proposed body changes rather than maintaining a second specification. Proposed changes remain pending; they enter the body only through an operator-approved update by `managing-projects` if that integration is chosen.

After a session compaction, re-read the checkpoint before continuing; it is the record, and your memory of the session is a lossy copy of it.

## Summaries

A **converged summary** is the exit:

```markdown
## Destination
## Decisions
- <question>: <answer>
## Out of scope
## Acceptance criteria
<For an issue, link to the body's criteria and list any proposed edits as pending; for a loose idea, state verifiable outcomes.>
## Files and artifacts
## Evidence
<prototype branches or standalone artifact paths, research citations>
## Follow-ups
## Blocked on
## Open questions
## Suggested skills
```

A **progress summary** is a pause. It holds Destination, Decisions so far, Open questions, Not yet specified (the fog you can't phrase as a question yet), and Candidate research. Starting the next session from it resumes the work.

## Finish

The exit criterion is a converged summary the operator confirms as a shared understanding. Write it as the final checkpoint and show it in chat. Ask whether to stop, hand off, or build; offer tracker integrations only when relevant:

1. **Stop or save for later:** leave the summary in the chosen checkpoint and name its path or URL. A lasting standalone record may live at an operator-chosen path without an issue.
2. **Fresh standalone session:** call the Skill tool for "handoff" with the converged summary as Payload, or a link to its durable record, and the operator's next assignment as Next session. Continuing this interview uses `/grill-with-research <issue-or-slug>`; another assignment needs no tracker workflow.
3. **Fresh session runs `managing-projects`, if chosen:** use this when the operator wants an issue created or its body reconciled with the confirmed design. Call the Skill tool for "handoff" with the issue body link as Payload and the summary link and pending changes in Live thread; without an issue, link to the chosen summary checkpoint as Payload. Set `/managing-projects <issue-or-slug>` as Next session; it obtains approval for the exact body change before implementation handoff.
4. **Fresh session runs `orchestrating`, if chosen** (issue only, when the confirmed design agrees with the authoritative body): call the Skill tool for "handoff" with a link to the issue body as Payload, the local summary path or authorized summary comment link in Live thread, and `/orchestrating #<n>` as Next session. Do not load `orchestrating` in this session. Tell the operator to open a new session, load `orchestrating`, and point it at the file.
5. **Build here:** only on the operator's explicit go-ahead. When an existing issue governs the build, its body must already contain the confirmed requirements; otherwise offer route 3 before implementation. A standalone build needs no issue.

The handoff document's Suggested skills section points to the summary's own. Done means the operator has picked a route and the route's artifact exists: the summary path or URL, the handoff file path in chat, or the build started. Choosing a route is not the handoff itself.

Save durable artifacts, such as glossary entries, ADRs, and scripts, at agreed destinations. When they belong to a repository, commit on the issue's linked branch when one exists, otherwise by repository convention. A branch exists only once there is something to commit on it.
