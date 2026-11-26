# Read-only roadmap data

## GitHub

Use `gh api`: `gh issue list` can't read milestone metadata or parent issues. `{owner}/{repo}` fills in from the current clone. For GitHub Enterprise Server, prefix the commands with `GH_HOST=<host>`.

- **Milestones:** `gh api --paginate "repos/{owner}/{repo}/milestones?state=all&per_page=100" --jq '.[] | {number, title, description, state, due_on, closed_at}'`. Milestones have no start date. `due_on` is a UTC timestamp, so take its date part.
- **Issues in a milestone:** `gh api --paginate "repos/{owner}/{repo}/issues?milestone=<number>&state=all&per_page=100" --jq '.[] | select(.pull_request == null) | {number, title, state, created_at, labels: [.labels[].name]}'`. The issues endpoint also returns pull requests, which the `select` drops.
- **Issues with no milestone:** the same call with `milestone=none&state=open`, adding `parent: (.parent_issue_url // null | if . then split("/") | last | tonumber else null end)` to group them by parent issue. GitHub Enterprise Server older than 3.16 has no sub-issues, so `parent` is always null there.

## GitLab

Use `glab api`: `glab milestone list` and `glab issue list` don't page through every result. `:fullpath` fills in from the current clone. For a self-hosted instance, set `GITLAB_HOST=<host>` or pass `--hostname <host>`.

- **Milestones:** `glab api --paginate "projects/:fullpath/milestones?include_ancestors=true"`. This returns active and closed milestones, including group milestones, each with `title`, `description`, `state`, `start_date`, and `due_date`.
- **Issues in a milestone:** `glab api --paginate "projects/:fullpath/milestones/<id>/issues"`. Each issue carries `labels` and `created_at`.
- **Issues with no milestone:** `glab api --paginate "projects/:fullpath/issues?milestone_id=None&state=opened"`. On Premium and Ultimate, group them by the issue's `epic`. On Free, use linked issues: `glab api "projects/:fullpath/issues/<iid>/links"`.

## Local Markdown

There are no milestones and no dates. Propose each `.scratch/<feature-slug>/` directory as a milestone, named from its `spec.md` title. Take the date the earliest issue file was added as the start suggestion: `git log --diff-filter=A --format=%as -- <file> | tail -1`, or the file's modification date when `.scratch/` is untracked. Have the operator confirm the grouping and supply every finish date.
