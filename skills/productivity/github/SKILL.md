---
name: github
description: "Unified GitHub skill: code review, issue/PR lifecycle, repo management, auth, CLI and REST workflows, templates, and scripts."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: ["GitHub", "Git", "CI/CD", "Code-Review", "Issues", "Pull-Requests", "Repositories", "Authentication"]
    related_skills: ["git", "terminal"]
---

# GitHub

Class-level umbrella for GitHub operations: authentication, code review, issues, pull requests, repository management, GitHub Actions, releases, secrets, gists, and raw API usage.

## When to use

Use this umbrella for interactions with GitHub through `gh`, `git`, or `curl`/REST. It replaces the narrower `github-auth`, `github-code-review`, `github-issues`, `github-pr-workflow`, and `github-repo-management` skills.

---

## 1. Authentication

See `github-auth` for original steps.

<!-- BEGIN_AUTH_SECTION -->
## 1. Authentication

Set up GitHub access using `gh`, Git credentials, HTTPS tokens, SSH keys, and plain `curl` with `GITHUB_TOKEN`.

### Detection

```bash
if command -v gh &>/dev/null && gh auth status &>/dev/null; then
  AUTH="gh"
else
  AUTH="git"
  if [ -z "$GITHUB_TOKEN" ]; then
    if [ -f ~/.hermes/.env ] && grep -q "^GITHUB_TOKEN=" ~/.hermes/.env; then
      GITHUB_TOKEN=$(grep "^GITHUB_TOKEN=" ~/.hermes/.env | head -1 | cut -d= -f2 | tr -d '\n\r')
    elif grep -q "github.com" ~/.git-credentials 2>/dev/null; then
      GITHUB_TOKEN=$(grep "github.com" ~/.git-credentials 2>/dev/null | head -1 | sed 's|https://[^:]*:\([^@]*\)@.*|\1|')
    fi
  fi
fi
```

### Input guarding

Validate any prompted file path against the actual filesystem before using it in a sensitive command.

```bash
if [ -e "$path" ]; then
  ...
else
  echo "Refusing to use $path: not present on disk"
  exit 1
fi
```

### Setup methods

- **HTTPS + PAT**: use GitHub Settings -> Developer settings -> Personal access tokens; store with `git config --global credential.helper store` or use token directly in the URL.
- **SSH key**: prefer `ed25519`; add public key in GitHub Settings -> SSH and GPG keys; test with `ssh -T git@github.com`.
- **gh CLI**: `gh auth login` for interactive setup; `gh auth login --with-token` for headless/token-based setup.

### Common issues

- Password auth is disabled; use a token.
- Cached credentials can expire; re-run `gh auth login` or clear `git credential reject`.
- Port 22 blocked? Switch SSH to HTTPS port `443` with `Host github.com` overrides.

## 2. Code Review

See `github-code-review` for original details.

<!-- BEGIN_CODE-REVIEW_SECTION -->

Use the GitHub code review workflow for pre-push diffs and PR reviews. Use `git diff main...HEAD` for local changes; fetch remote PRs locally with `git fetch origin pull/123/head:pr-123 && git checkout pr-123`.

After review, submit comments and formal approvals through the official tool. Record review outputs as reviews, not as general approvals even if a reviewer approval of a reviewer is required.

Use a structured verdict: Critical, Warnings, Suggestions, Looks Good.

<!-- END_CODE-REVIEW_SECTION -->

## 3. Issues

See `github-issues` for original details.

<!-- BEGIN_ISSUES_SECTION -->

View, create, label, assign, comment, and close GitHub issues. Use `gh issue list`, `gh issue create`, `gh issue edit`, and `gh issue close` commands where available.

Apply common templates for bug reports and feature requests.

<!-- END_ISSUES_SECTION -->

## 4. Pull Request Lifecycle

See `github-pr-workflow` for original details.

<!-- BEGIN_PR_WORKFLOW_SECTION -->

Follow branch, commit, push, PR creation, CI monitoring, merge, and cleanup workflows. Use `gh pr checks --watch` or the `/check-runs` REST endpoint to track CI.

Auto-fix CI loops by reading failed logs, patching code, committing, pushing, and re-checking status.

Branch naming: `feat/`, `fix/`, `refactor/`, `docs/`, `ci/`.

Merge with `--squash` by default; prefer `--auto` when conditions are clear.

<!-- END_PR_WORKFLOW_SECTION -->

## 5. Repository Management

See `github-repo-management` for original details.

<!-- BEGIN_REPO_MGMT_SECTION -->

Manage repository creation, cloning, forking, sync, settings, branch protection, secrets, releases, GitHub Actions workflows, and gists.

Use `gh secret set NAME --body "value"` for secrets. REST requires repo-owned public-key encryption, so `gh` is preferred there.

<!-- END_REPO_MGMT_SECTION -->

## 6. Raw API Usage

<!-- BEGIN_RAW_API_SECTION -->

When `gh` is unavailable, use REST with `GITHUB_TOKEN` sourced from `~/.hermes/.env`, `~/.git-credentials`, or environment variables. Every section above documents the curl fallback.

<!-- END_RAW_API_SECTION -->

## 7. GitHub Actions Workflows

<!-- BEGIN_ACTIONS_SECTION -->

Use `gh workflow list`, `gh run list`, `gh run view`, `gh run rerun`, and `gh workflow run` to manage GitHub Actions. REST endpoints remain available under `owner/repo/actions/...`.

<!-- END_ACTIONS_SECTION -->

## 8. Pull conflict resolution — untracked files

When `git pull` fails with:
```
error: The following untracked working tree files would be overwritten by merge:
  <file>
Please move or remove them before you merge.
Aborting.
```

This happens when an untracked file exists locally AND a tracked version arrives from the remote. Common with shared workspaces (e.g. Smith repo synced between Mac and Antigravity).

**Resolution steps:**
1. Check the local file: `wc -l <file>` + `cat <file>` — is it a stub or has real content?
2. Check the remote version: `git show origin/master:<file>`
3. If the remote has more content (typical — the remote version came from a real session), back up local and pull:
   ```bash
   mv <file> <file>.local-bak
   git pull origin master
   ```
4. If local has more content, stash it: `mv <file> <file>.local-override` and merge manually after pull.

**Pitfall:** Don't blindly `rm` the local file — always check content first. A 3-line stub vs a 20-line real log is the common case, but occasionally the local file has unique work.

## 9. Extracting Raw File Contents from Repos

When researching a GitHub repo and you need actual file contents (not just metadata), use raw URLs:

```bash
# Fetch a single file
curl -s https://raw.githubusercontent.com/OWNER/REPO/BRANCH/path/to/file.md

# Example: get README
curl -s https://raw.githubusercontent.com/buildermethods/agent-os/main/README.md

# Example: get a specific command file
curl -s https://raw.githubusercontent.com/buildermethods/agent-os/main/commands/agent-os/discover-standards.md

# Fetch multiple files in parallel
cd /target/dir && \
curl -s https://raw.githubusercontent.com/OWNER/REPO/main/file1.md > file1.md && \
curl -s https://raw.githubusercontent.com/OWNER/REPO/main/file2.md > file2.md
```

**Workflow for repo research:**
1. **Browser** → navigate to repo, understand structure (README, file tree)
2. **Terminal + curl** → fetch raw files in bulk (faster than browser clicks)
3. **Save locally** → copy into project structure

**Pitfall:** Don't use `gh api /repos/.../contents/...` for raw file content — it returns base64-encoded JSON. Use `raw.githubusercontent.com` instead for direct text.

**When to use:** Extracting templates, configs, command definitions, or reference files from repos you're studying or forking concepts from.

## 10. Consolidated quick reference

| Action | Preferred |
|--------|---------|
| Auth status | `gh auth status` |
| PR checks | `gh pr checks` |
| PR review | `gh pr review` |
| PR diff | `gh pr diff` |
| Issue list | `gh issue list` |
| Issue create | `gh issue create` |
| Repo create | `gh repo create` |
| Secret | `gh secret set` |
| Workflow rerun | `gh run rerun` |

Use REST fallbacks from the sections above when `gh` is unavailable.
