---
name: research
description: Investigate a question against high-trust primary sources with parallel researcher subagents and report cited findings. Use when the operator wants a topic researched, docs or API facts gathered, or reading legwork delegated.
metadata:
  upstream:
    repo: "https://github.com/mattpocock/skills"
    author: Matt Pocock
    license: MIT
---

1. **Settle the scope.** If the goal or scope is unclear, load `grilling` and grill until you can state what the research must answer. If the question is already precise, skip this step.
2. **Decompose.** Split the question into research questions, each one independent, bounded, and answerable from sources. Propose the list to the operator, and wait for approval before dispatching anything.
3. **Prepare access.** Complete the **Capability check** below for each approved question before dispatching it.
4. **Route.** Load `model-routing` and apply its tier-selection rules to each approved question.
5. **Dispatch.** Spin up one `researcher` subagent with its explicitly routed model per ready question, all in parallel. Give each exactly one question, the intent behind it, its completion boundary, the confirmed tools and sources it may use, and any prepared evidence packet. Assign only work those tools and sources can support; state unresolved access gaps explicitly.
6. **Report.** Reconcile the findings into one report in chat. Answer the operator's original question first, then give each research question's finding with its citations. Name conflicts between researchers and gaps any of them reported; never paper over them.

Write the report to a file only when the operator or a calling skill explicitly asks for one. Save it where the repo already keeps such notes, match the existing convention, and say where it went.

## Capability check

Apply this check before every researcher dispatch, including investigations called directly by another skill.

1. **Confirm tools.** Inspect the active researcher profile and the harness tool catalog. The role is read-only. Confirm which sources its file, web, or read-only git tools can actually read; tool availability depends on the profile. The bundled Pi profile has file access only. Do not assume the child can use the coordinator's tools or authentication. When access cannot be confirmed, prepare evidence centrally rather than dispatching an access probe.
2. **Prepare evidence.** For authenticated APIs, private tracker records, or CLI-only facts, the coordinator collects primary evidence within the approved read boundary before dispatch. Put a sanitized packet in a scratchpad file the researcher can read, with observation timestamps, source URLs or identifiers, the read commands or endpoints, and relevant response fields. Keep credentials and sensitive data outside the packet and assignment; ask before expanding access or the read boundary.
3. **Check readiness.** Every fact needed for the completion boundary must be reachable through confirmed researcher tools or the prepared packet. If required evidence remains unavailable, pause that question and report the blocker; ask whether to narrow it to available evidence when that would change the approved boundary. A narrowed assignment states what remains unverified. The researcher cites original sources and packet observations, distinguishes current from historical evidence, and reports remaining gaps; missing access is not a reason to escalate the model.
