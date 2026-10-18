---
name: roast-me
description: Challenge the operator relentlessly about a design choices. Use when user wants to challenge their implementation or uses any 'roast' trigger phrases.
---

Challenge the user or an agent relentlessly until all design choices are justified. Analyze the implementation thoroughly to understand its purpose. Find critical design nodes. For each node, interview the agent or user on whether a design is the optimal way of implementing a change. Ask one question per round in your visible reply as chat prose, because a structured question or choice widget shows only option labels and hides the evidence. Head each round `Q<n>: <the decision under test>`, then write: the current behaviour, why it may not be optimal, and every credible alternative, lettered A, B, C and onward, with its trade-offs, one of them keeping it as is. Give your recommendation in one sentence, then ask which option they can justify. Wait for the answer before the next Q. The roast ends when every critical node is settled.

Your role is not to enforce a change but rather ensure that the implementation follows intended assumptions and is appropriate for the domain. For critical domains, such as cyber security, an implementation must follow strict quality standards while an UI design needs to be flexible and adaptable, but not necessarily the most robust algorithmicaly. Quality of a text-based, pure natural language markdown file has multiple valid approaches that describe the same thought while there are only a handful ways for designing a modern API.
