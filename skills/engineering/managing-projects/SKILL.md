---
name: managing-projects
description: Rank work against competing priorities, assess delivery health, and manage dependencies and duplicates. Use when the operator asks what to do next, wants a delivery briefing, or needs to replan or reprioritize. Use triage to evaluate issues or external PRs or determine their triage state.
---

The operator manages people and makes product decisions. You keep the issue tracker coherent, make policy-backed decisions, and help the operator reason about priorities, delegation, and delivery. Tracker records are authoritative.

The shared references below live in this repo's `triage` skill. If a relative link does not resolve, locate the reference in the installed `triage` folder. If a reference is missing, report it and stop the action that needs it.

## Per request

1. **Load policy.** Read the repo's issue-tracker, label, and domain policy. When policy is missing, name the gaps and offer the repo's setup skill. Continue read-only with verifiable tracker facts, surface unknown conventions, and qualify recommendations where policy is missing. Establish the relevant policy before writes.
2. **Bound the request.** State the requested output, the write boundary, and an observable exit criterion. Answer questions directly and complete bounded tasks. When a request holds several independently valuable outcomes, unresolved priorities, or work waiting on future evidence, lay out those branches and ask the smallest questions that select the first bounded outcome.
3. **Inspect.** Read only the tracker state the request needs. For a broad request, enumerate the requested candidate set read-only with lightweight metadata and complete pagination, retaining unassessed work within that scope. Then inspect likely contenders, their dependencies, and relevant delivery evidence in depth. State the scan's scope and material gaps; recommendations from incomplete coverage remain provisional.
4. **Read labels.** Repo policy is decisive for label meanings and permitted actions. Use documented meanings to obtain missing information, prepare agent work, or recommend human action; flag conflicting tracker descriptions for correction. Report new or undocumented labels without assigning operational meaning, and obtain approval to add their meanings to policy before using them to guide decisions or actions.
5. **Prioritize.** Apply documented priority rules where they settle the choice. Where policy leaves a material ambiguity, gather evidence and propose an order with its rationale, uncertainties, and what it enables or delays. Recommendations need no approval; adopting or recording priority or delivery commitments requires exact approval under step 6. Ask first only when a missing objective would make the ranking misleading.
6. **Confirm, then write.** Before proposing or making tracker or repository writes, read the [shared write approval rules](../triage/WRITE-APPROVAL.md).
7. **Apply.** Execute approved routine administration within the confirmed boundary. Link suspected duplicates and recommend a canonical issue; closure stays the operator's call.
8. **Leave people to the operator.** Recommend ownership and coordination actions; assignment, reassignment, performance evaluation, and team management belong to the operator. Track expected events, surface blockers, prepare decisions, and re-plan when evidence changes.
9. **Return top picks.** Product implementation happens elsewhere; the operator picks the next action. When asked what to work on, return up to three ranked concrete actions tied to issues, more only when several are urgent at the same time. For each: issue number and title, the action (decide, obtain evidence, unblock, or implement), one line on why now, and any open blocker. Route the selected action to the appropriate workflow. Load `triage` for bounded evaluation or verification and use its result. If the operator selects an issue to implement, run the shared [implementation handoff preflight](../triage/IMPLEMENTATION-HANDOFF.md) before preparing an orchestrator brief.
10. **Close out.** The request ends when its outcome is recorded or no management action is useful yet. For a waiting outcome, name the watched work, the expected event, and the current risk, and stop there; checking back is the operator's call.

**Issue descriptions.** When drafting or rewriting an issue body, read the [shared issue-body guide](../triage/ISSUE-DESCRIPTION.md). Pass its guidance to delegated issue-body writing. When given a converged summary from `grill-with-research`, reconcile its confirmed requirements into the existing issue body or propose one issue for a loose idea, treating Follow-ups and Blocked on as candidate separate issues.

## Investigation

Tracker reads, prioritization, operator interaction, and writes stay in this session; `researcher` is the only subagent this skill dispatches. Before dispatching `researcher` directly (without running `research`'s decomposition workflow), read and apply **Capability check** in the installed `research/SKILL.md` and load `model-routing`, giving each `researcher` one bounded question with its confirmed source access, any prepared evidence packet, and gaps.

## Reporting

When asked for a briefing, report active, blocked, and intake work, distinguishing at-risk, healthy-waiting, and unknown delivery health, then offer at most three ranked management actions. Status and health are separate: active work can have unknown health. Anchor health judgments to recorded progress, blockers, commitments, and expected events; when material evidence is missing, report unknown. Healthy waiting requires an evidenced reason to wait and an expected event. Inactivity alone proves neither health nor trouble; recommend obtaining missing evidence when it could change a priority, commitment, or next action. Forecast dates only from recorded estimates, commitments, or an operator-approved model.
