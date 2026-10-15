---
name: setup-engineering-skills
description: "Configure this repo for the engineering skills: capture project context and set up its issue tracker, label vocabulary, and domain doc layout. Run once before first use of the other engineering skills."
disable-model-invocation: true
---

# Setup Engineering Skills

Scaffold the per-repo configuration that the engineering skills assume:

- **Project context**: a short description in the repo's root agent instruction file, alongside the policy links
- **Issue tracker**: where issues live (GitHub by default; local markdown is also supported out of the box)
- **Labels**: the strings used for the five canonical triage roles, plus any category or priority labels this repo's tracker already carries
- **Domain docs**: where `GLOSSARY.md` and ADRs live, and the consumer rules for reading them (single-GLOSSARY only — this variant has no map layout)
- **Verification**: the test and check commands agents run, when `orchestrating` is installed

This is a prompt-driven skill, not a deterministic script. Explore, present what you found, confirm with the user, then write.

## Process

### 1. Explore

Look at the current repo to understand its starting state. Read whatever exists; don't assume:

- `git remote -v` and `.git/config`: is this a GitHub, GitHub Enterprise Server, or GitLab repo? Which one, and which host?
- `AGENTS.md` and `CLAUDE.md` at the repo root: does either exist? Is there already an `## Agent skills` section in either? Identify any existing project description, whether under `## Project` or elsewhere.
- `README.md` and relevant project docs: what evidence is there for the project's purpose, audience, responsibilities, and non-goals?
- `GLOSSARY.md` at the repo root and `docs/adr/`
- `docs/agents/`: does this skill's prior output already exist?
- `.scratch/`: a sign that a local-markdown issue tracker convention is already in use
- Existing tracker labels (`gh label list` / `glab label list`, or ask if neither CLI is available): do labels beyond the five triage roles already exist — a bug/enhancement/decision-style category split, or a priority scale? Their presence decides whether Section B offers those extra tiers.
- Is the `triage` skill installed? (a `triage` skill folder alongside this one, or `triage` in your available skills.) This decides whether Section B runs at all.
- Is the `orchestrating` skill installed? This decides whether Section D runs. If it is, also check for a GitHub Project linked to the repo (`gh project list --owner <owner>`), existing `todo` / `in-progress` labels, and any documented branch naming convention (`CONTRIBUTING.md`, `AGENTS.md`, `CLAUDE.md`), plus test and check commands for Section E.

### 2. Present findings and ask

Summarise what's present and what's missing. Then take the sections in order. One section, one answer, then the next.

Lead each section with the recommended answer so the user can accept it in a word. Give a one-line explainer only when the choice genuinely branches; skip the section entirely when exploration already settled it (Section B when `triage` isn't installed).

**Project context.** Before Section A, ask these three questions one at a time, leading each with an answer suggested by repository evidence. Ask the user to confirm or correct it; where the repo leaves a gap, ask rather than inventing an answer.

1. What does this project do?
2. Who is it for?
3. What are its main responsibilities and explicit non-goals?

If a project description already exists, first propose keeping it or revising it. Keeping it satisfies this section; revising it uses the three questions to settle the changes. Preserve the existing description unless the user approves a revision, and include any proposed move or consolidation in the draft.

Condense confirmed answers into 2–4 sentences for `## Project` in the root instruction file selected in step 4. Keep this inline, alongside `## Agent skills`; the existing policy configuration and links stay intact. Include the description in step 3's draft before writing.

**Section A: Issue tracker.**

> Explainer: The "issue tracker" is where issues live for this repo. Some skills read from and write to it. They need to know whether to call `gh issue create`, write a markdown file under `.scratch/`, or follow some other workflow you describe. Pick the place you actually track work for this repo.

Default posture: these skills were designed for GitHub. Read the hostname in the `git remote` URL, not just whether it's `github.com`: a self-hosted host still names its platform (`gitlab.example.com`, `*.ghe.com`). If it points at `github.com`, propose GitHub. If the hostname contains `gitlab`, propose GitLab (self-hosted or `gitlab.com` alike). If the hostname contains `github` (a GitHub Enterprise Server instance) or is otherwise unrecognized, propose GitHub Enterprise Server and confirm the hostname with the user before recording it. Otherwise (or if the user prefers), offer:

- **GitHub**: issues live in the repo's GitHub Issues (uses the `gh` CLI)
- **GitHub Enterprise Server**: same as GitHub, but on a self-hosted instance. `gh` doesn't always resolve a self-hosted host from the git remote the way it does for `github.com`, so every command needs `GH_HOST=<host>` set first. Ask for the hostname (e.g. `novonordisk.ghe.com`) and record it.
- **GitLab**: issues live in the repo's GitLab Issues (uses the [`glab`](https://gitlab.com/gitlab-org/cli) CLI)
- **Local markdown**: issues live as files under `.scratch/<feature>/` in this repo (good for solo projects or repos without a remote)
- **Other** (Jira, Linear, etc.): ask the user to describe the workflow in one paragraph; the skill will record it as freeform prose

Record the choice in `docs/agents/issue-tracker.md`. The GitHub and GitLab templates carry a "PRs as a request surface" flag, defaulted **off**. Leave it off and don't raise it: a user who wants external PRs in the triage queue can flip the flag in the file later. Each template also carries a **Workflow state** section: keep it only when Section D runs, and delete it otherwise. Keep the **Roadmap data** section as is; `roadmap` reads it.

**Section B: Label vocabulary.** Skip this section entirely if the `triage` skill isn't installed (exploration told you), since an uninstalled skill needs no labels.

If it is installed, first ask about the triage roles:

> Do you want to keep the default triage labels? (recommended: **yes**)

The defaults are the five canonical roles, each label string equal to its name: `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`. On **yes**, write them as-is. Only if the user says no, usually because their tracker already uses other names (e.g. `bug:triage` for `needs-triage`), collect the overrides so `triage` applies existing labels instead of creating duplicates.

Then, only if exploration found labels beyond the five roles, offer to document them as additional tiers rather than inventing new ones:

- **Category tier** (what kind of work): if `bug`/`enhancement`-style labels exist, offer to record them alongside a `decision` role for decision tickets — issues resolved by choosing an answer, not by shipping a deliverable.
- **Priority tier** (how urgent): if a priority scale exists (Linear-style or otherwise), offer to record it as `p0`–`p4`, where `p0` means "not yet assessed" rather than "most urgent."

If neither tier's labels exist in the tracker, skip both silently — don't create labels the repo doesn't use.

**Section C: Domain docs.** Single-GLOSSARY only: one `GLOSSARY.md` + `docs/adr/` at the repo root. Write it without asking — this variant of the skill has no multi-GLOSSARY or map layout to offer.

**Section D: Workflow state.** Skip this section entirely if the `orchestrating` skill isn't installed. It fills the **Workflow state** section of `docs/agents/issue-tracker.md`, which `orchestrating` requires before it starts.

- **State.** If exploration found a project board, propose recording it: its name or URL and its in-progress column. Otherwise propose the fallback labels `todo` and `in-progress`; a closed issue counts as done, so there is no `done` label. Create any missing fallback labels once the user confirms.
- **Branch naming.** If exploration found a documented convention, propose recording it. Otherwise propose the fallback `<type>/<issue-id>-<slug>`, where type is `feature`, `bugfix`, or `hotfix`.

**Section E: Verification.** Skip this section entirely if the `orchestrating` skill isn't installed. Propose the targeted-test, full-suite, and static-check commands found in exploration (`package.json` scripts, `Makefile`, `pyproject.toml`, CI workflows, `CONTRIBUTING.md`), and ask for the full suite's typical duration and any environment needs or slow, flaky, or interfering fixtures. Record them in `docs/agents/verification.md`; specialists and reviewers run these instead of rediscovering them.

### 3. Confirm and edit

Show the user a draft of:

- The `## Project` section, or the existing description to keep, including any proposed move or consolidation
- The `## Agent skills` block to add to the same `CLAUDE.md` / `AGENTS.md` (see step 4 for selection rules)
- The contents of `docs/agents/issue-tracker.md`, `docs/agents/domain.md`, `docs/agents/labels.md` (only when `triage` is installed), and `docs/agents/verification.md` (only when `orchestrating` is installed)

Let them edit before writing.

### 4. Write

**Pick the file to edit:**

- If `CLAUDE.md` exists, edit it.
- Else if `AGENTS.md` exists, edit it.
- If neither exists, ask the user which one to create; don't pick for them.

Never create `AGENTS.md` when `CLAUDE.md` already exists (or vice versa); always edit the one that's already there.

For a new description, add this section in the same file before `## Agent skills`:

```markdown
## Project

[2–4 confirmed sentences about purpose, audience, main responsibilities, and explicit non-goals.]
```

When keeping an existing description, leave it unchanged in its current location. When revising, update it in-place; move or consolidate it into `## Project` only as approved in step 3. If none exists, add the section once. Preserve unrelated instruction text.

If an `## Agent skills` block already exists in the chosen file, update its contents in-place rather than appending a duplicate. Don't overwrite user edits to the surrounding sections.

The block:

```markdown
## Agent skills

### Issue tracker

[one-line summary of where issues are tracked]. See `docs/agents/issue-tracker.md`.

### Labels

[one-line summary of the label vocabulary]. See `docs/agents/labels.md`.

### Domain docs

Single-GLOSSARY (`GLOSSARY.md` and `docs/adr/` at root). See `docs/agents/domain.md`.

### Verification

Targeted, full-suite, and static-check commands. See `docs/agents/verification.md`.
```

Include the `### Labels` sub-block, and write `docs/agents/labels.md`, only when `triage` is installed and Section B ran. When it isn't, both are omitted. Include the `### Verification` sub-block, and write `docs/agents/verification.md`, only when `orchestrating` is installed and Section E ran.

Then write the docs files using the seed templates in this skill folder as a starting point:

- [issue-tracker-github.md](./issue-tracker-github.md): GitHub or GitHub Enterprise Server issue tracker (substitute the captured hostname if Enterprise)
- [issue-tracker-gitlab.md](./issue-tracker-gitlab.md): GitLab issue tracker
- [issue-tracker-local.md](./issue-tracker-local.md): local-markdown issue tracker
- [labels.md](./labels.md): label mapping — triage roles always; category and priority tiers only if Section B found and confirmed them
- [domain.md](./domain.md): domain doc consumer rules, single-GLOSSARY layout
- [verification.md](./verification.md): verification commands, only when Section E ran

For "other" issue trackers, write `docs/agents/issue-tracker.md` from scratch using the user's description.

### 5. Done

Tell the user the setup is complete and which engineering skills will now read from these files. Mention they can edit `docs/agents/*.md` directly later; re-running this skill is only necessary if they want to switch issue trackers or restart from scratch.
</content>
