import tempfile
from pathlib import Path

from changeloggen.core import Commit, get_latest_tag


def test_commit_category_parsing():
    c = Commit(hash="abc123", message="feat: add login", author="me", date="2026-01-01")
    assert c.category == "feat"
    assert c.title == "add login"


def test_commit_with_scope():
    c = Commit(hash="abc123", message="fix(api): handle timeout", author="me", date="2026-01-01")
    assert c.category == "fix"
    assert c.title == "handle timeout"


def test_commit_no_prefix():
    c = Commit(hash="abc123", message="random change", author="me", date="2026-01-01")
    assert c.category == "other"
    assert c.title == "random change"


def test_get_commits_from_own_history():
    """Integration test: reads commits from the actual repo."""
    repo = Path(__file__).resolve().parents[3]  # takopi root
    from changeloggen.core import get_commits
    commits = get_commits(repo, from_ref="HEAD~3", to_ref="HEAD")
    assert len(commits) >= 1
    assert all(isinstance(c, Commit) for c in commits)


def test_get_latest_tag():
    repo = Path(__file__).resolve().parents[3]
    tag = get_latest_tag(repo)
    assert tag.startswith("v")
