---
name: commit
description: "Commit working-tree changes as atomic commits (one reason to revert each), with subjects that match the repo's message convention and `type(scope): summary` as the default. Commits locally only: never pushes or opens pull requests. Use when committing changes, splitting work into several commits, amending the latest commit, or writing a commit message or subject line."
---

A commit is **atomic**: one reason to revert, so one type and one scope. Reason-to-revert outranks type: tests, docs, fixtures, and migrations that exist only because of a change share its commit, and the type follows the production change. Use `test` for coverage of code that already exists and `docs` for documentation of behavior that already shipped.

Work is done when every hunk in the requested scope has landed in exactly one commit and every other changed hunk is named in the report as left in the tree. The scope comes from the caller's assignment or the operator; with none given, everything that doesn't look foreign is in scope. This skill never pushes.

When asked only for a message or subject line, do steps 3–5.

1. **Survey the whole diff** before touching `git commit` — `git status`, then `git diff` and `git diff --staged`. Read the hand-written hunks, not just the filenames: for a deleted or wholly rewritten file, read what was there (`git show HEAD:<path>`), since its contents decide which group it joins. Classify generated content (lockfiles, snapshots, build output) by its cause: check it with `git diff --stat` plus the change that explains it, and group it with that change.

   Untracked paths and tracked hunks unrelated to the request each need a decision — commit, ignore, leave, or ask when the call isn't yours to make (content whose real home is outside the repo, generated session state, someone else's work in progress). Ask if an operator is present; otherwise leave it in the tree and report it.

2. **Group the hunks into atomic commits.** Split by reason-to-revert, not by file: a refactor and the feature it enables are two commits even in one file, and a rename touching thirty files is one. Every hunk in scope is assigned to exactly one commit before you commit anything.

   Stage whole files by path. Where a file mixes purposes, trim `git diff -- <path>` to the hunks of one group and apply it with `git apply --cached --recount <patch>`; for interleaved hunks, edit the patch by hand first. This keeps file modes, handles new and deleted files, and leaves the working tree holding the final content. If a clean split needs more than a recount-level edit, commit the tangled hunks together and say why in the body.

   Each commit in a batch should parse. For a batch of more than one commit, check the **staged** content, not the working tree, which holds the final state and passes regardless: export the index with `git checkout-index -a --prefix=<temp-dir>/` into a temporary directory outside the repo and run the repo's documented fast check (typecheck, lint, build) there. Where no such check exists, or it needs dependencies the export lacks, parse-check the staged files individually or report the commit as unverified.

3. **Detect the convention.** Read `git log --pretty=%s -50` and look for a commitlint config. If most subjects match `type(scope):` or a config exists, follow it: reuse the scope vocabulary in use and match its casing. If the history uses another style, match that style and say so in the report. Use `type(scope):` only when the history is empty. For a new area, name the directory or module that owns the change; leave the scope off when the change is genuinely repo-wide. If a `commit-msg` hook or config disagrees with this skill, the repo wins.

4. **Write the subject** as `type(scope): imperative summary` — imperative mood ("add", "drop", "fix"), lowercase after the colon, no trailing period, 72 characters or fewer. Types: `feat`, `fix`, `refactor`, `perf`, `style` (formatting only), `docs`, `test`, `build`, `ci`, `chore`, `revert`. Mark a breaking change with `!` before the colon and add a `BREAKING CHANGE:` footer to the body.

5. **Add a body** when the diff shows the what but not the why — the reason for the change, the alternative rejected, the trade-off accepted. Wrap at 72 characters. Mechanical changes ship subject-only. Add no trailers (such as `Co-authored-by`) unless the operator asks or the repo's history already uses them.

6. **Commit each group in order**, staging explicitly by path or patch so the staged set matches the subject you just wrote. Then confirm with `git status` that nothing in scope is still sitting in the working tree.

   If a hook fails, read its output, fix the cause, restage, and make a new commit. Never pass `--no-verify`. If a hook rewrote files, rerun `git status` and fold the changes into the same group before moving on. If the failure can't be fixed, stop and report which commits landed and which didn't.

7. **Amend** the latest commit only when the change belongs to it (reverting that commit should also undo this change), it is unpushed, and it is yours. Never amend after a failed hook: no commit was created, so `--amend` would rewrite the previous one. If the amended commit's subject no longer fits, rewrite it.

8. **Report** to whoever invoked you, briefly: commits made, hunks left in the tree, commits not verified.
