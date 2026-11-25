---
name: grill-with-research
description: Converge a foggy idea or issue into one fixed-scope work item through grilling, research, and prototypes. Works standalone, ending in a converged summary; tracker integrations are optional.
disable-model-invocation: true
---

`grill-with-research` turns a foggy idea into one **fixed-scope work item**: a destination, the decisions that pin it, and testable acceptance criteria someone can later pick up and build. The interview and summary need no repository policy, tracker setup, or issue. You converge through grilling, research, and prototypes within the session. Tracker publication and collaboration with `managing-projects` or `orchestrating` are optional.

## Start

1. **Load the input.** For an issue, read [Tracker integration](TRACKER-INTEGRATION.md) for issue input and the publication boundary. For a handoff document or a pasted summary, resume from its open questions and fog. Otherwise take the loose idea as stated.
2. **Choose the record.** Use local checkpoints by default; issue publication follows the tracker reference. Pass the chosen boundary to loaded skills.
3. **Name the provisional destination.** Load `grilling` and `domain-modeling`. Fact-gathering within grilling follows the Research rule below. Without an agreed glossary or ADR destination, capture vocabulary and decisions in the summary. The first round establishes the desired outcome and constraints; the destination stays provisional while evidence-dependent decisions remain open.
4. **Draft candidate research.** Tie each research question to the decision it informs and the facts needed to settle it.

## Converge

Run grilling rounds until the frontier is empty. Within the rounds:

- **Read back** each ambiguous or garbled answer: state your interpretation and have the operator confirm it in the next round before anything builds on it.
- **Evidence.** Follow [Research](#research) for factual uncertainty and [Prototype](#prototype) when experiential evidence can answer a named uncertainty.
- **Scope.** When the idea holds several work items, narrow to one and record the rest as follow-ups.
- **Blocked on someone else.** Work only another person can do goes under Blocked on, with a precise checklist for them.

After about six rounds, offer to pause with a progress summary; the operator may continue.

## Research

1. Resolve straightforward facts directly through read-only inspection.
2. For substantive investigations, propose the decision-linked question list in the current round and wait for approval.
3. Check delegation prerequisites before choosing that path: valid assignment-specific routing configuration, an available researcher profile with usable source access, and runtime support for explicit model selection.
   - **Available:** load `research` with the already-approved list and access boundary; that approval satisfies its question-list approval step, while changed scope needs fresh approval. Actual dispatches must pass `model-routing` and research's Capability check.
   - **Absent or invalid:** report the limitation and perform the approved read-only investigation in-session instead.
4. Both paths retain primary-source citations, evidence gaps, and the approved access boundary.
5. Gather findings before asking the operator to choose an option that depends on them; continue independent frontier questions while research is pending. Findings land in chat and shape the next round.
6. When evidence invalidates an assumption, reopen the affected decision and any decisions that depended on it.

## Prototype

1. Use concrete scenarios for questions answerable in prose.
2. When running or seeing something can resolve a named uncertainty, identify the question and the decision it will settle, then load `prototype`. The call is exploration-only: capture validated decisions in the summary; the prototype skill's production-integration step waits for a separately authorized build.
3. Choose isolation before building, keeping the operator's checkout untouched:
   - **Repository-dependent prototypes:** use a separate worktree on a throwaway `prototype/<slug>` branch.
   - **Standalone demos:** use the scratchpad.
4. Build the smallest prototype that answers the question within the round, and have the operator pick in the next.
5. Commit repository-dependent prototypes on that branch. Record the question, verdict, and branch or standalone artifact path under Evidence.

## Checkpoint

Write the running summary before dispatching research or a prototype, after a session compaction, and at session end:

- **Local:** load `handoff` with the running summary as Payload and `grill-with-research <issue-or-slug>` as the next assignment. The temp directory may lose it; for a lasting record, save the summary at an operator-chosen path and use a link to that record as Payload. A durable summary needs no issue.
- **Issue publication, when authorized:** follow [Tracker integration](TRACKER-INTEGRATION.md#checkpoints).

After a session compaction, re-read the checkpoint before continuing; it is the record, and your memory of the session is a lossy copy of it.

## Summaries

A **converged summary** is the exit:

```markdown
## Destination
## Decisions
- <question>: <answer>
## Out of scope
## Acceptance criteria
<State verifiable outcomes; issue-backed summaries follow the Acceptance criteria rule in TRACKER-INTEGRATION.md.>
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

The exit criterion is an operator-confirmed converged summary recorded in the chosen checkpoint and shown in chat. This completes the interview. Offer relevant next steps without requiring a choice; execute a chosen handoff or explicitly authorized build as a separate assignment:

1. **Stop or save for later:** leave the summary in the chosen checkpoint and name its path or URL. A lasting standalone record may live at an operator-chosen path without an issue.
2. **Fresh standalone session:** load `handoff` with the converged summary as Payload, or a link to its durable record, and the operator's next assignment as Next session. Continuing this interview uses `grill-with-research <issue-or-slug>`; another assignment needs no tracker workflow.
3. **Tracker-backed handoff, if chosen:** read [Tracker integration](TRACKER-INTEGRATION.md#handoffs) for `managing-projects` or `orchestrating`.
4. **Build here:** only on the operator's explicit go-ahead. A standalone build needs no issue; when an existing issue governs the build, follow the tracker reference's [Implementation boundary](TRACKER-INTEGRATION.md#implementation-boundary).

The handoff document's Suggested skills section points to the summary's own. A chosen handoff is complete only when its file exists and its path is shown in chat. Choosing a route is not the handoff itself.

Save durable artifacts, such as glossary entries, ADRs, and scripts, at agreed destinations. When they belong to a repository, commit on the issue's linked branch when one exists, otherwise by repository convention. A branch exists only once there is something to commit on it.
