---
name: grill-with-research
description: Converge a foggy idea or issue into one fixed-scope work item through grilling, research, and prototypes, ending in a converged summary.
disable-model-invocation: true
---

`grill-with-research` turns a foggy idea into one **fixed-scope work item**: a destination, the decisions that pin it, and testable acceptance criteria someone can later pick up and build. You converge through grilling, research, and prototypes, running research and prototypes within grill-with-research rather than spinning them off as separate issues. On the tracker you read and post one summary comment; creating issues, applying labels, and editing issue bodies belong to `managing-projects`.

## Start

1. **Load the input.** For an issue, read its body, comments, sub-issues, dependencies, and linked branch; its original purpose bounds the destination, and an earlier grill-with-research summary comment is where you resume. For a handoff document or a pasted summary, resume from its open questions and fog. Otherwise take the loose idea as stated.
2. **Name the provisional destination.** Call the Skill tool for "grilling" and "domain-modeling". The first round establishes the desired outcome and constraints; the destination stays provisional while evidence-dependent decisions remain open.
3. **Draft candidate research.** Tie each research question to the decision it informs and the facts needed to settle it.

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

- **Issue:** one summary comment, created at the first checkpoint and edited in place after that. Link to the authoritative body; record decisions, evidence, and proposed body changes rather than maintaining a second specification. Proposed changes remain pending until `managing-projects` applies the operator-approved body update.
- **Loose idea:** call the Skill tool for "handoff" with the running summary as Payload and `/grill-with-research <slug>` as Next session. The temp directory may lose it; a summary that must last needs an issue, which `managing-projects` creates.

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

The exit criterion is a converged summary the operator confirms as a shared understanding. Write it as the final checkpoint and show it in chat. Then ask how to hand off, offering these routes:

1. **Fresh session runs `orchestrating`** (issue only, when the confirmed design agrees with the authoritative body): call the Skill tool for "handoff" with a link to the issue body as Payload, the summary comment link in Live thread, and `/orchestrating #<n>` as Next session. Do not load `orchestrating` in this session. Tell the operator to open a new session, load `orchestrating`, and point it at the file.
2. **Fresh session runs `managing-projects`:** required when confirmed scope or acceptance criteria still need a body update. Call the Skill tool for "handoff" with the issue body link as Payload and the summary link and pending changes in Live thread; for a loose idea, use the converged summary as Payload. Set `/managing-projects` as Next session; it obtains approval and updates the existing issue body or creates an issue before implementation.
3. **Build here:** only on the operator's explicit go-ahead; for an existing issue, the body must already contain the confirmed requirements, otherwise use route 2 first.
4. **Stop:** the summary stays on the issue, or in the loose-idea handoff document, for a later session.

The handoff document's Suggested skills section points to the summary's own. Done means the operator has picked a route and the route's artifact exists: the handoff file path in chat, the issue updated, or the build started. Choosing a route is not the handoff itself.

Commit durable artifacts, such as glossary entries, ADRs, and scripts, on the issue's linked branch when one exists, otherwise by repository convention. A branch exists only once there is something to commit on it.
