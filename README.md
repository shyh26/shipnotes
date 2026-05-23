# changeloggen

Generate beautiful changelogs from git history. Conventional commits in, user-friendly release notes out.

## What it does

You write [conventional commits](https://www.conventionalcommits.org/). changeloggen reads your git history and turns it into a clean, categorized changelog your users will actually read.

## Quick start

```bash
pip install changeloggen
changeloggen generate
```

## Example output

```markdown
## v1.2.0 (2026-05-20)

### Features
- Add dark mode support
- Introduce export to CSV

### Bug Fixes
- Fix login redirect loop on Safari
- Handle empty search results gracefully

### Documentation
- Update API reference for v2 endpoints
```

## Features

- **Conventional commit parsing** — Auto-categorizes by type (feat, fix, docs, etc.)
- **Tag-aware** — Scopes changelog to commits since last tag
- **Markdown output** — Ready to paste into GitHub Releases
- **Custom categories** — Map commit types to your own section names

## Supported commit types

| Prefix | Category |
|--------|----------|
| `feat:` / `feature:` | Features |
| `fix:` / `bugfix:` | Bug Fixes |
| `perf:` | Performance |
| `refactor:` | Refactoring |
| `docs:` | Documentation |
| `test:` | Tests |
| `chore:` | Chores |
| `ci:` | CI/CD |
| `style:` | Style |

## Tech stack

Python, Typer, Rich, Git
