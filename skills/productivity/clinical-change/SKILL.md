---
name: clinical-change
description: Make an edit that contains nothing beyond what the outcome requires. Use when the operator asks for a narrowly scoped change ("just change X", "only fix Y", "don't touch anything else"), or when an edit must not include refactoring, cleanup, or formatting beyond what the outcome requires.
---

Apply a **clinical change**: every hunk in the diff is necessary for the outcome, and nothing else appears.

- **Necessary:** the requested edit would fail to work, build, or pass existing checks without it. This includes updated callers and imports, tests the change breaks, and formatting the project's formatter or CI requires. If the outcome cannot be met within the obvious lines, expand only as far as necessary, without asking. If you expanded, say what and why in one sentence.
- **Not necessary:** refactors, cleanups, adjacent fixes, and formatter churn on lines the outcome never touched. Do not comment on these.
- Edit with targeted replacement. Never rewrite the whole file.
- After editing, inspect the diff and revert any hunk that is not necessary.

## Example

Request: "Rename the exported function `getUser` to `fetchUser`."

- Clinical: the definition and every call site and import of `getUser` change, and nothing else. Report: "Also updated 4 call sites in `api/` and `ui/`, since the rename breaks them."
- Not clinical: the same rename, plus reordered imports in the touched files, reformatted call sites, a fixed typo in a nearby comment, or `getUsers` renamed for consistency.
