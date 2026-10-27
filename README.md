# Skills for Staying in Charge

Composable agent skills for engineers, project managers and everyone else who works with a coding agent. Subagents start on the cheapest model tier that can do the job and escalate only with a stated reason. Every implementation step gets a fresh session, and a reviewer who did not write the code checks the result.

Each skill stands alone. Start from whichever fits your situation and skip the rest. They compose in any order, but none requires another.

## Installation

### 1. Get the skills

Install the upstream skills these depend on, then this repo.

```sh
npx skills@latest add mattpocock/skills   # select grill-with-docs, grilling, domain-modeling, prototype
npx skills@latest add A-NGJ/skills
```

Or install this repo manually:

```sh
git clone git@github.com:A-NGJ/skills.git ~/src/a-ngj-skills
cd ~/src/a-ngj-skills
for s in skills/{engineering,productivity}/*/; do ln -s "$PWD/${s%/}" ~/.claude/skills/"$(basename "$s")"; done
```

Use `~/.agents/skills/` instead of `~/.claude/skills/` if your agent harness reads that directory.

Requirements: `git`, and `gh` for GitHub or `glab` for GitLab. A local markdown tracker (`.scratch/`) needs neither.

`commit`, `explain`, `clinical-change`, `roast-me` and `grill-with-research` work after this step.

### 2. Supply the agents and `.model-routing`

Only `orchestrating`, `research` and `managing-projects` dispatch subagents. They need the agent profiles and a `.model-routing` file. See [Agents](#agents).

### 3. Run `/setup-engineering-skills`

Run it once per repo, only if you want the tracker workflow (`orchestrating`, `managing-projects`, `triage`, `to-tickets`). It asks what the project does, who it serves, and its main responsibilities and non-goals, suggesting answers from the repo for you to confirm. It puts the confirmed description under `## Project` in `AGENTS.md` or `CLAUDE.md`.

It also configures your issue tracker (GitHub, GitLab or local markdown), label vocabulary and domain docs, writing `docs/agents/issue-tracker.md` and `docs/agents/domain.md`, plus `docs/agents/labels.md` when `triage` is installed and `docs/agents/verification.md` when `orchestrating` is installed. `orchestrating` refuses to start until `issue-tracker.md` has a **Workflow state** section.

## Why These Skills Exist

I built these skills to fix failure modes I see when working with coding agents.

### #1: The Agent Didn't Build What I Meant

**The Problem**. You think the agent knows what you want. Then you see what it built, and it did not understand you at all. The idea was still foggy when the work started.

**The Fix** is to resolve the fog before any code is written:

- [`/grill-with-research`](skills/productivity/grill-with-research/SKILL.md) turns a foggy idea or issue into one fixed-scope work item with testable acceptance criteria, through grilling, research and prototypes.
- [`/roast-me`](skills/productivity/roast-me/SKILL.md) interviews you on each critical design choice in an existing implementation, until you can justify it or record it as unsettled.

### #2: Every Subagent Runs on the Same Model

**The Problem**. Delegating work to subagents does not help if every subagent is the most expensive model. A file search does not need what a security review needs, and the daily limit is gone after the first issue.

**The Fix** is to route each assignment to a model tier. [`model-routing`](skills/engineering/model-routing/SKILL.md) reads the repository's `.model-routing` file, picks the lowest tier that can meet the assignment's completion boundary, and escalates only with a stated reason. Reviews have a tier floor. A missing or invalid route stops the dispatch, and there is no silent fallback to another model.

### #3: The Agent Changed More Than I Asked

**The Problem**. You ask for a rename and get a rename, reordered imports, a reformatted call site and a "fixed" comment. The diff is too big to review, and too tangled to revert.

**The Fix** is to keep each change small and justified:

- [`/clinical-change`](skills/productivity/clinical-change/SKILL.md) makes an edit where every hunk is necessary for the outcome and nothing else appears.
- [`/commit`](skills/engineering/commit/SKILL.md) splits the work into atomic commits, with one reason to revert each.
- [`/pr`](skills/engineering/pr/SKILL.md) writes a pull request body with a summary, before/after evidence, manual testing steps and a merge-danger call.

### #4: I Don't Know What To Work On Next

**The Problem**. The tracker grows faster than anyone reads it. Issues are duplicated, blocked on each other, or too big to start, and ranking them by hand takes the time you wanted to spend on the work.

**The Fix** is to put the tracker through a small set of skills:

- [`managing-projects`](skills/engineering/managing-projects/SKILL.md) ranks next actions, manages dependencies and duplicates, and prepares a brief for the next issue.
- [`triage`](skills/engineering/triage/SKILL.md) moves each issue or external PR through triage roles and writes agent-ready briefs.
- [`to-tickets`](skills/engineering/to-tickets/SKILL.md) splits a plan into tracer-bullet issues with blocking edges.

### #5: The Context Window Ran Out Mid-Task

**The Problem**. One session holds the plan, the implementation and the review. Its context fills with stale detail, quality drops, and you end up restarting sessions by hand and acting as the orchestrator yourself.

**The Fix** is [`/orchestrating`](skills/engineering/orchestrating/SKILL.md). It plans one issue once, then runs each step in a fresh implementation-specialist session on one shared worktree branch. A fresh reviewer checks each checkpoint, and the run ends at a pull request. You answer decisions and nothing else. Model tiers come from `model-routing`, which is why #2 and #5 belong together. [`handoff`](skills/productivity/handoff/SKILL.md) covers the cases where you move between sessions by hand.

### Typical flow

None of these steps is required, and each skill works on its own:

```text
grill-with-research -> triage / to-tickets -> managing-projects -> orchestrating -> pull request
```

## How This Differs From Matt's Skills

These skills build on [mattpocock/skills](https://github.com/mattpocock/skills), which are excellent, and they install next to them. Four of them are upstream dependencies. The rows below describe design differences, so you can pick the version that suits your situation.

| Area | Upstream | This repo |
| --- | --- | --- |
| `triage`, `to-tickets` | Operator-invoked only. | Model-invokable, so `managing-projects` can call them. |
| `handoff` | Operator-invoked only. Free-form document with a suggested-skills section. | Model-invokable. Fixed skeleton, stable path `$TMPDIR/handoff/<skill>-<target>.md`, and a receiving rule that re-reads every linked tracker record before acting. |
| `research` | One background agent writes a Markdown file in the repo. | Fans the question out to parallel `researcher` subagents, each routed to a model tier, and reports cited findings. |
| `pr` | Summary, Evidence and Merge Danger. | Adds a Manual Testing section and an Undo field, which `orchestrating` relies on. |
| `grill-with-docs` and `grill-with-research` | `grill-with-docs` loads `grilling` and `domain-modeling`. | `grill-with-research` adds research and prototypes, and ends in a converged summary. It works without a tracker. |
| `implement-spec` and `orchestrating` | Works a whole spec as a task graph on one integration branch, with parallel implementer subagents in their own worktrees. | Works one issue sequentially on one shared worktree branch, with a fresh reviewer at each checkpoint, and ends at a pull request. |
| Model selection | Not part of `implement-spec`'s dispatch. | `model-routing` selects a tier for every dispatch from `.model-routing`. |
| Only here | | `model-routing`, `managing-projects`, `clinical-change`, `roast-me`, `explain` |

Use upstream's `implement-spec` when you want parallel throughput. Use `orchestrating` when you want a gated, sequential run.

`triage`, `to-tickets`, `research`, `pr` and `handoff` share names with upstream. Do not install both copies, because the callers in this repo rely on the differences above. Upstream `grill-with-docs` also stops the model from loading it, so the skills here load `grilling` and `domain-modeling` directly. Run `/grill-with-docs` yourself when you want a grilling session that updates `GLOSSARY.md` and ADRs.

## Reference

Skills are grouped by who they serve. Within each group, **operator-invoked** skills set `disable-model-invocation`, so only you can start them with a slash command. **Model-invoked** skills can also be loaded by the model or by other skills.

### Engineering

**Operator-invoked**

- **[orchestrating](skills/engineering/orchestrating/SKILL.md)**: Plans one issue into steps, implements each step in a fresh specialist session in one worktree, reviews the result, then opens a pull request. Requires a clean worktree before every dispatch and one active orchestrator per issue. Its rules, correction budget and exits are in the skill.
- **[setup-engineering-skills](skills/engineering/setup-engineering-skills/SKILL.md)**: Captures project context and configures a repo: tracker, labels, domain docs, workflow states. Run once per repo.

**Model-invoked**

- **[commit](skills/engineering/commit/SKILL.md)**: Atomic commits with `type(scope):` subjects.
- **[pr](skills/engineering/pr/SKILL.md)**: Template for pull request bodies: summary, evidence, manual testing, merge danger.
- **[model-routing](skills/engineering/model-routing/SKILL.md)**: Resolves a required repository model route per agent and tier before dispatch.

### Project management

**Model-invoked**

- **[managing-projects](skills/engineering/managing-projects/SKILL.md)**: Ranks priorities, manages dependencies and duplicates, and picks the next issue with a brief for the orchestrator.
- **[triage](skills/engineering/triage/SKILL.md)**: Moves issues and external PRs through triage roles and writes agent-ready briefs.
- **[to-tickets](skills/engineering/to-tickets/SKILL.md)**: Splits a plan into tracer-bullet issues with blocking edges.

### Productivity

**Operator-invoked**

- **[grill-with-research](skills/productivity/grill-with-research/SKILL.md)**: Converges a foggy idea into one fixed-scope work item through grilling, research and prototypes. Works standalone, ending with a converged summary; tracker integrations are optional.
- **[roast-me](skills/productivity/roast-me/SKILL.md)**: A relentless interview that challenges whether each design choice is justified.

**Model-invoked**

- **[handoff](skills/productivity/handoff/SKILL.md)**: Writes a handoff document to the OS temp directory so a fresh session can continue the work.
- **[research](skills/productivity/research/SKILL.md)**: Fans a question out to parallel `researcher` subagents and reports cited findings.
- **[explain](skills/productivity/explain/SKILL.md)**: Explains a topic step by step with one concrete example before the general rule, pitched at the audience.
- **[clinical-change](skills/productivity/clinical-change/SKILL.md)**: Makes an edit that contains nothing beyond what the outcome requires.

### Agents

The skills expect these externally supplied roles, with one definition each. This repository ships skills, not agent definitions, so supply the profiles in your runtime. A profile may omit a model or have a default; routed dispatches always use the explicit repository route instead.

| Role | Permissions | Used by |
| --- | --- | --- |
| `implementation-specialist` | Plan mode reads only and returns an implementation plan; step mode edits and commits one step in the issue worktree. Cannot dispatch other agents. | `orchestrating` |
| `reviewer` | Read-only. Returns `Accepted`, `Changes Required`, or `Needs clarification`. | `orchestrating` |
| `researcher` | Read-only, no shell. Reads files and the web. | `research`, `managing-projects` |

Configure `.model-routing` at the repository's main checkout as a JSON map from agent IDs to `fast`, `standard` and `deep` model references. The model references below are placeholders; agent IDs and reference syntax must match your runtime:

```json
{
  "researcher": {
    "fast": "provider/researcher-fast-model",
    "standard": "provider/researcher-standard-model",
    "deep": "provider/researcher-deep-model"
  }
}
```

Add one entry per agent the coordinator will dispatch, including the built-in agents. See [`model-routing`](skills/engineering/model-routing/SKILL.md) for the required-route gate and the reviewer tier floor. The file is a skill convention, not native runtime configuration, so the runtime must support explicit model selection at dispatch.

### Layout

```text
skills/<group>/<name>/SKILL.md   one folder per skill, grouped engineering/ or productivity/
skills/<group>/<name>/agents/    Codex display metadata (openai.yaml)
skills/in-progress/              skills not yet ready for release
skills/engineering/setup-engineering-skills/
                                 templates for GitHub, GitLab and local trackers, labels and domain docs
LICENSE                          MIT license for this repo
LICENSES/                        upstream license texts
GLOSSARY.md                      shared vocabulary for handoff documents and their payloads
```

## Credits and licenses

MIT, see [`LICENSE`](LICENSE).

`triage`, `to-tickets`, `research`, `pr` and `handoff` are adapted from [Matt Pocock's skills](https://github.com/mattpocock/skills) (MIT, see `LICENSES/mattpocock-skills.txt`). Each carries a `metadata.upstream` entry in its frontmatter. The `pr` summary section comes from Dex Horthy's [`show-me`](https://github.com/humanlayer/humanlayer), described in `skills/engineering/pr/CREDITS.md`.
