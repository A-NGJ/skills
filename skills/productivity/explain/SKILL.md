---
name: explain
description: Feynman style. Use when the operator asks to "explain", "walk me through", or "help me understand".
---

# Feynman-style explanations

## Explain

Infer the operator's knowledge from the conversation and state the assumed
level when it changes the answer. Ask one brief question only when nothing in
the conversation indicates a level and the topic spans several (a first
message like "explain transformers").

Explain what happens and why each step follows. For a mechanism, show what
changes, what causes that change, and how it produces the result. For an
abstract topic, show the relationships or reasoning that make the idea work.
A label such as "energy" or "market forces" needs an explanation of the
relevant process.

Keep precise domain vocabulary. Define terms on first use, including
standard ones the operator may not know.

Default to a core answer in two or three sentences that states the cause and
the effect, then one concrete example walked end-to-end, then the general
rule. Open with the definition or statement when the question asks for one.

When using an analogy, identify what corresponds to the real topic and state
any limitation that could mislead.

## Verify

Before answering, test each step: can you state what causes it without using
its name? Put that cause in the answer. If you can't, add a "Simplified:" or
"Unverified:" note saying what you are simplifying or don't know, instead of
letting the name stand in for the explanation. Add notes only when there is
something to report.

Distinguish an observed rule from a known mechanism when it matters, and
state the assumptions and limits that affect the answer.

Look something up when the answer depends on a version, a number, or a quote,
or when you can't state the mechanism in plain words. Otherwise answer from
what you know and state the assumption.

Exit criterion: every step states its cause or carries a Simplified/Unverified
note, and every version, number, or quote is looked up or marked Unverified.

## Quick check

After a substantive explanation, end with one brief "Quick check" only when
the operator is learning the topic: "teach me", "why does", "I don't get", or
a topic unrelated to their current task. Skip it when the explanation serves
a task in progress (a stack trace, a diff, an error), for factual
clarifications, or when the operator wants only an answer.

Change one condition in the example or the rule, and ask the operator to
predict the result. Leave the answer for their reply.

If the next message answers the check, say whether it is right and name the
step it depends on, then revise only the part the answer shows was missed.
If the next message is about something else, drop the check.
