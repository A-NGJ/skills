# skills

Composable agent skills and subagents for working an issue tracker: researching, scoping, prioritizing and implementing issues. The issue tracker is the record: skills read and write issues, labels and comments, and keep no state of their own.

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

Then install this repo's skills with one of the two methods below, and the agents by hand.

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

The `agents/` folder holds opencode subagent definitions. Link them from a clone, whichever method you used for the skills.

```sh
for f in agents/*.md; do ln -s "$PWD/$f" ~/.config/opencode/agents/"$(basename "$f")"; done
```

Every agent file ships with `model: ""`. Set a model in each one before use. See [Agents](#agents-1) for why the tiers matter.

### Per-repo setup

In each repo you want to use these skills on, run `/setup-engineering-skills` once. It asks for your issue tracker (GitHub, GitLab or local markdown), your label names and where domain docs live. It writes `docs/agents/issue-tracker.md`, `docs/agents/labels.md` and `docs/agents/domain.md`, and adds an `## Agent skills` block to `AGENTS.md` or `CLAUDE.md`. `orchestrating` refuses to start until `issue-tracker.md` has a **Workflow state** section.

## Skills

Skills marked "operator" set `disable-model-invocation`, so only you can start them with a slash command. The rest can also be loaded by the model or by other skills.

| Skill | Started by | What it does |
| --- | --- | --- |
| `setup-engineering-skills` | operator | Configures a repo: tracker, labels, domain docs, workflow states. |
| `managing-projects` | either | Ranks priorities, manages dependencies and duplicates, and picks the next issue with a brief for the orchestrator. |
| `wayfinding` | operator | Converges a foggy idea into one fixed-scope work item through grilling, research and prototypes. Ends with a summary comment. |
| `orchestrating` | operator | Runs the implement and review loop on one issue in a worktree, then opens a pull request. Stops after three `Changes Required` verdicts. |
| `roadmap` | either | Builds a milestone roadmap from the tracker as theme swimlanes over weeks, in Markdown, HTML or PowerPoint. |
| `model-routing` | either | Picks the fast, standard or deep agent tier before a subagent is dispatched. |
| `triage` | either | Moves issues and external PRs through triage roles and writes agent-ready briefs. |
| `to-tickets` | either | Splits a plan into tracer-bullet issues with blocking edges. |
| `research` | either | Fans a question out to parallel `researcher` subagents and reports cited findings. |
| `pr` | either | Template for pull request bodies: summary, evidence, manual testing, merge danger. |
| `commit` | either | Atomic commits with `type(scope):` subjects. |

## Agents

Three roles, each in three tiers. `model-routing` chooses the tier per assignment.

| Role | Tiers | Permissions | Used by |
| --- | --- | --- | --- |
| `implementation-specialist` | fast, standard, deep | Edits and commits in the issue worktree. Cannot dispatch other agents. | `orchestrating` |
| `reviewer` | fast, standard, deep | Read-only. Returns `Accepted` or `Changes Required`. | `orchestrating` |
| `researcher` | fast, standard, deep | Read-only, no shell. Reads files and the web. | `research`, `managing-projects` |

Tier suffixes are `-fast` and `-deep`; the standard tier has no suffix. The variants of one role share instructions and differ only in `model`.

`model-routing` never lets a `reviewer` run on the same model as the `implementation-specialist` it reviews. If you give both roles the same model in every tier, the rule cannot be satisfied, so use at least two different models.

## Upstream dependencies

These skills come from [mattpocock/skills](https://github.com/mattpocock/skills) and are not copied here.

| Skill | Used by |
| --- | --- |
| `grilling` | `wayfinding`, `managing-projects`, `research`, `triage` |
| `domain-modeling` | `wayfinding`, `managing-projects`, `triage` |
| `prototype` | `wayfinding`, `managing-projects` |
| `grill-with-docs` | You, as the entry point for design interviews. |

Upstream `grill-with-docs` sets `disable-model-invocation`, which stops the model from loading it. For that reason the skills in this repo load `grilling` and `domain-modeling` directly instead of calling `grill-with-docs`. Run `/grill-with-docs` yourself when you want a grilling session that updates `GLOSSARY.md` and ADRs.

Do not install upstream `triage`, `to-tickets`, `research` or `pr` next to this repo. They share names with the copies here, and the upstream versions differ:

- `triage` and `to-tickets` set `disable-model-invocation`, so `managing-projects` cannot call them.
- `research` runs one background agent and ignores the `researcher` tiers.
- `pr` lacks the Manual Testing section and the Undo field that `orchestrating` relies on.

## Layout

```text
agents/                  opencode subagents, three roles x three tiers
skills/<name>/SKILL.md   one folder per skill
skills/<name>/agents/    Codex display metadata (openai.yaml)
skills/roadmap/render.py roadmap renderer (md, html, pptx)
skills/setup-engineering-skills/
                         templates for GitHub, GitLab and local trackers, labels and domain docs
LICENSES/                upstream license texts
```

## Credits and licenses

`triage`, `to-tickets`, `research` and `pr` are adapted from [Matt Pocock's skills](https://github.com/mattpocock/skills) (MIT, see `LICENSES/mattpocock-skills.txt`). Each carries a `metadata.upstream` entry in its frontmatter. The `pr` summary section comes from Dex Horthy's [`show-me`](https://github.com/humanlayer/humanlayer), described in `skills/pr/CREDITS.md`.

This repo has no license of its own yet.
