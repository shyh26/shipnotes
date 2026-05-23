from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Commit:
    hash: str
    message: str
    author: str
    date: str

    @property
    def category(self) -> str:
        m = re.match(r"(\w+)(?:\(.*\))?:", self.message)
        return m.group(1).lower() if m else "other"

    @property
    def title(self) -> str:
        return re.sub(r"^\w+(?:\(.*\))?:\s*", "", self.message)


@dataclass
class Changelog:
    version: str
    date: str = ""
    entries: dict[str, list[str]] = field(default_factory=dict)

    def add(self, category: str, line: str) -> None:
        self.entries.setdefault(category, []).append(line)


CATEGORY_LABELS: dict[str, str] = {
    "feat": "Features",
    "fix": "Bug Fixes",
    "perf": "Performance",
    "refactor": "Refactoring",
    "docs": "Documentation",
    "test": "Tests",
    "chore": "Chores",
    "ci": "CI/CD",
    "other": "Other Changes",
}


def get_commits(repo: Path, from_ref: str = "", to_ref: str = "HEAD") -> list[Commit]:
    """Get commits between two refs."""
    range_spec = f"{from_ref}..{to_ref}" if from_ref else to_ref
    cmd = ["git", "-C", str(repo), "log", range_spec,
           "--format=%H%n%s%n%an%n%ai%n---"]
    try:
        output = subprocess.check_output(cmd, text=True, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        return []

    commits = []
    for block in output.split("---"):
        lines = block.strip().split("\n")
        if len(lines) >= 4:
            commits.append(Commit(
                hash=lines[0][:8],
                message=lines[1],
                author=lines[2],
                date=lines[3][:10],
            ))
    return commits


def get_latest_tag(repo: Path) -> str:
    """Get the latest git tag."""
    try:
        return subprocess.check_output(
            ["git", "-C", str(repo), "describe", "--tags", "--abbrev=0"],
            text=True, stderr=subprocess.DEVNULL,
        ).strip()
    except subprocess.CalledProcessError:
        return ""


def generate(repo: Path | None = None, from_ref: str = "", to_ref: str = "HEAD",
             version: str = "") -> Changelog:
    """Generate a changelog from git history."""
    repo = repo or Path.cwd()
    if not from_ref:
        from_ref = get_latest_tag(repo)
    if not version:
        version = to_ref

    commits = get_commits(repo, from_ref, to_ref)
    cl = Changelog(version=version)
    for c in commits:
        cat = CATEGORY_LABELS.get(c.category, "Other Changes")
        cl.add(cat, f"{c.title} ({c.hash})")

    return cl
