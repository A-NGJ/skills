# skills

Composable agent skills for working an issue tracker: researching, scoping, prioritizing and implementing issues. The issue tracker is the record: skills read and write issues, labels and comments, and keep no state of their own.

Each skill stands alone. Start from whichever fits your situation and skip the rest.

- **`research`**: you need facts from docs, APIs or code, gathered with citations.
- **`wayfinding`**: an idea or issue is still foggy and needs to become one fixed-scope work item.
- **`managing-projects`**: you don't know what to work on next, or the tracker needs re-ranking.
- **`orchestrating`**: the issue is clear and you want it implemented, reviewed and opened as a pull request.

They compose in any order, but none requires another. For example, `orchestrating` works on any issue you name, whether or not `wayfinding` touched it first. The one prerequisite is running `setup-engineering-skills` once per repo, because `orchestrating` won't start without it.

## Requirements

- `git`
- `gh` for GitHub or `glab` for GitLab. A local markdown tracker (`.scratch/`) needs neither.
- `uv`, only for `roadmap`. `render.py` declares its `python-pptx` dependency inline.
- Four skills from [mattpocock/skills](https://github.com/mattpocock/skills). See [Upstream dependencies](#upstream-dependencies).

## Install

Install the [upstream dependencies](#upstream-dependencies) first:

```sh
npx skills@latest add mattpocock/skills   # select grill-with-docs, grilling, domain-modeling, prototype
```

Then install this repo's skills with one of the two methods below, and configure the required agents in your runtime.

### skills CLI

```sh
npx skills@latest add A-NGJ/skills
```

### Manual

```sh
git clone git@github.com:A-NGJ/skills.git ~/src/a-ngj-skills
cd ~/src/a-ngj-skills
for s in skills/*/; do ln -s "$PWD/${s%/}" ~/.claude/skills/"$(basename "$s")"; done
```

Use `~/.agents/skills/` instead of `~/.claude/skills/` if your agent harness reads that directory.

### Agents

This repository ships skills, not agent definitions. Supply the required agent profiles in your runtime, with one definition per role. A profile may omit a model or have a default; routed dispatches always use the explicit repository route instead. See [Agents](#agents-1) for the roles and setup requirements. The runtime must support explicit model selection at dispatch.

### Per-repo setup

In each repo you want to use these skills on, run `/setup-engineering-skills` once. It asks what the project does, who it serves, and its main responsibilities and non-goals, suggesting answers from the repo for you to confirm. It puts the confirmed 2–4 sentence description under `## Project` in `AGENTS.md` or `CLAUDE.md`, alongside the existing `## Agent skills` policy links. Existing project context is kept or revised only with your approval.

The existing setup also configures your issue tracker (GitHub, GitLab or local markdown), label vocabulary and domain docs. It writes `docs/agents/issue-tracker.md` and `docs/agents/domain.md`, plus `docs/agents/labels.md` when `triage` is installed and `docs/agents/verification.md` (test and check commands) when `orchestrating` is installed. `orchestrating` refuses to start until `issue-tracker.md` has a **Workflow state** section.

## Skills

Skills marked "operator" set `disable-model-invocation`, so only you can start them with a slash command. The rest can also be loaded by the model or by other skills.

| Skill | Started by | What it does |
| --- | --- | --- |
| `setup-engineering-skills` | operator | Captures project context and configures a repo: tracker, labels, domain docs, workflow states. |
| `managing-projects` | either | Ranks priorities, manages dependencies and duplicates, and picks the next issue with a brief for the orchestrator. |
| `wayfinding` | operator | Converges a foggy idea into one fixed-scope work item through grilling, research and prototypes. Ends with a converged summary. |
| `orchestrating` | operator | Plans one issue into steps, implements each step in a fresh specialist session in one worktree, reviews the result, then opens a pull request. Stops after three `Changes Required` verdicts per issue. |
| `roadmap` | either | Builds a milestone roadmap from the tracker as theme swimlanes over weeks, in Markdown, HTML or PowerPoint. |
| `model-routing` | either | Resolves a required repository model route per agent and tier before dispatch. |
| `triage` | either | Moves issues and external PRs through triage roles and writes agent-ready briefs. |
| `to-tickets` | either | Splits a plan into tracer-bullet issues with blocking edges. |
| `research` | either | Fans a question out to parallel `researcher` subagents and reports cited findings. |
| `pr` | either | Template for pull request bodies: summary, evidence, manual testing, merge danger. |
| `commit` | either | Atomic commits with `type(scope):` subjects. |
| `handoff` | either | Writes a handoff document to the OS temp directory so a fresh session can continue the work. `wayfinding` calls it to save a loose idea's progress and to hand off to `orchestrating` or `managing-projects`. |
| `explain` | either | Explains a topic step by step with one concrete example before the general rule, pitched at the audience. Triggers on "explain" or "clarify". |

## Agents

The skills expect these externally supplied roles, with one definition each. `model-routing` keeps the agent ID fixed and selects a model per assignment.

| Role | Permissions | Used by |
| --- | --- | --- |
| `implementation-specialist` | Plan mode reads only and returns an implementation plan; step mode edits and commits one step in the issue worktree. Cannot dispatch other agents. | `orchestrating` |
| `reviewer` | Read-only. Returns `Accepted` or `Changes Required`. | `orchestrating` |
| `researcher` | Read-only, no shell. Reads files and the web. | `research`, `managing-projects` |

Configure `.model-routing` at the repository's main checkout as a JSON map from agent IDs to `fast`, `standard`, and `deep` model references. Built-in agents can have their own entries alongside custom roles. See [`model-routing`](skills/model-routing/SKILL.md) for the format, required-route gate, and reviewer tier floor. Missing or invalid routes block dispatch; agent defaults and global maps are not fallbacks.

The file is a skill convention, not native runtime configuration. The coordinator must be able to select the routed model explicitly when dispatching. Existing installations should keep one profile per role and remove old `-fast` and `-deep` copies after preserving their model choices in repository routes. Removing the templates from this repository does not migrate or delete installed profiles.

## Upstream dependencies

These skills come from [mattpocock/skills](https://github.com/mattpocock/skills) and are not copied here.

| Skill | Used by |
| --- | --- |
| `grilling` | `wayfinding`, `managing-projects`, `research`, `triage` |
| `domain-modeling` | `wayfinding`, `managing-projects`, `triage` |
| `prototype` | `wayfinding`, `managing-projects` |
| `grill-with-docs` | You, as the entry point for design interviews. |

Upstream `grill-with-docs` sets `disable-model-invocation`, which stops the model from loading it. For that reason the skills in this repo load `grilling` and `domain-modeling` directly instead of calling `grill-with-docs`. Run `/grill-with-docs` yourself when you want a grilling session that updates `GLOSSARY.md` and ADRs.

Do not install upstream `triage`, `to-tickets`, `research`, `pr` or `handoff` next to this repo. They share names with the copies here, and the upstream versions differ:

- `triage` and `to-tickets` set `disable-model-invocation`, so `managing-projects` cannot call them.
- `research` runs one background agent and ignores the `researcher` tiers.
- `pr` lacks the Manual Testing section and the Undo field that `orchestrating` relies on.
- `handoff` sets `disable-model-invocation`, so other skills cannot call it, and it lacks the fixed skeleton and stable path the callers rely on.

## Layout

```text
skills/<name>/SKILL.md   one folder per skill
skills/<name>/agents/    Codex display metadata (openai.yaml)
skills/roadmap/render.py roadmap renderer (md, html, pptx)
skills/setup-engineering-skills/
                         templates for GitHub, GitLab and local trackers, labels and domain docs
LICENSES/                upstream license texts
GLOSSARY.md              shared vocabulary for handoff documents and their payloads
```

## Credits and licenses

`triage`, `to-tickets`, `research`, `pr` and `handoff` are adapted from [Matt Pocock's skills](https://github.com/mattpocock/skills) (MIT, see `LICENSES/mattpocock-skills.txt`). Each carries a `metadata.upstream` entry in its frontmatter. The `pr` summary section comes from Dex Horthy's [`show-me`](https://github.com/humanlayer/humanlayer), described in `skills/pr/CREDITS.md`.

This repo has no license of its own yet.
