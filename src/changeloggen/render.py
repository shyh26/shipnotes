from __future__ import annotations

from .core import Changelog


def to_markdown(cl: Changelog) -> str:
    """Render a changelog as Markdown."""
    lines = [f"## {cl.version}", ""]
    if cl.date:
        lines.append(f"*{cl.date}*")
        lines.append("")

    for cat, entries in cl.entries.items():
        lines.append(f"### {cat}")
        lines.append("")
        for e in entries:
            lines.append(f"- {e}")
        lines.append("")

    return "\n".join(lines).strip()
