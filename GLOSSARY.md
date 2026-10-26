# Skills

Composable agent skills for working an issue tracker. These terms name the outputs passed between agent sessions.

## Language

**Handoff document**:
A temporary write-up that lets a fresh agent session continue the work, holding context not worth a tracker record.
_Avoid_: handoff file, session notes, checkpoint file

**Payload**:
The contract a skill passes inside a handoff document: one of the named briefs or summaries below, or a link to the tracker record holding it.
_Avoid_: content, body

**Orchestrator brief**:
A payload that tells an orchestrator which issue to implement, why now, and its completion boundary quoted from the issue.
_Avoid_: brief block, start prompt

**Alignment gate**:
The final check that the operator and orchestrator share an understanding of an issue's outcome, scope, acceptance criteria, chosen design, and consequential assumptions or trade-offs.
_Avoid_: quick grilling, preflight grilling

**Implementation plan**:
The output of an implementation specialist's plan mode: each acceptance criterion mapped to its current state and gap, ordered steps, operational steps, and consequential choices.
_Avoid_: task list, breakdown

**Step**:
One ordered unit of an implementation plan, implemented by a fresh implementation specialist session on the shared issue branch.
_Avoid_: subtask, phase

**Agent brief**:
A tracker comment that is the authoritative specification an AFK agent works from when an issue is ready for an agent.
_Avoid_: spec comment, ticket brief

**Converged summary**:
The record of a finished grill-with-research session: destination, decisions, scope, and testable acceptance criteria for one work item.
_Avoid_: final summary, grill-with-research output

**Progress summary**:
The record of a paused grill-with-research session: destination, decisions so far, open questions, and remaining fog.
_Avoid_: partial summary, draft summary
