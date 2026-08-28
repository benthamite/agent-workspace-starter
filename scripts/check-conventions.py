#!/usr/bin/env python3
"""Check the mechanical subset of the workspace conventions.

Covers the rules from projects/context/project-doc-conventions.md that can be
checked deterministically: every project has a brief and a map; Current focus
bullets carry TODO wording verbatim (no paraphrase); Current focus has no
dates and stays under the word cap; Current state has no session narrative;
meeting back-links resolve. Run from anywhere inside the workspace; exits
non-zero on any failure.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WORD_CAP = 130  # conventions say ~120; allow slack before failing


def section(text, heading):
    m = re.search(
        rf"^## {re.escape(heading)}\n(.*?)(?=^## |\Z)", text, re.M | re.S
    )
    return m.group(1) if m else None


def normalize(s):
    s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s)  # [text](url) -> text
    s = re.sub(r"[`*_]", "", s)
    return re.sub(r"\s+", " ", s).strip().lower()


def map_bullets(focus):
    """Yield bullet texts from Current focus, joining wrapped lines."""
    current = None
    for line in focus.splitlines():
        if line.strip().startswith("- "):
            if current is not None:
                yield current
            current = line.strip()[2:]
        elif current is not None and line.startswith(" ") and line.strip():
            current += " " + line.strip()
        else:
            if current is not None:
                yield current
            current = None
    if current is not None:
        yield current


def main():
    errors = []
    projects_dir = ROOT / "projects"
    for proj in sorted(p for p in projects_dir.iterdir() if p.is_dir()):
        if proj.name == "context":
            continue
        brief_path = proj / f"{proj.name}.md"
        map_path = proj / "CLAUDE.md"
        if not brief_path.exists():
            errors.append(f"{proj.name}: missing brief {brief_path.name}")
            continue
        if not map_path.exists():
            errors.append(f"{proj.name}: missing CLAUDE.md map")
            continue
        brief = brief_path.read_text(encoding="utf-8")
        map_text = map_path.read_text(encoding="utf-8")

        todos = section(brief, "Active TODOs")
        if todos is None:
            errors.append(f"{proj.name}: brief has no '## Active TODOs' section")
        todos_norm = normalize(todos or "")

        focus = section(map_text, "Current focus")
        if focus is None:
            errors.append(f"{proj.name}: map has no '## Current focus' section")
        else:
            words = len(focus.split())
            if words > WORD_CAP:
                errors.append(
                    f"{proj.name}: Current focus is {words} words (cap ~120)"
                )
            if re.search(r"\d{4}-\d{2}-\d{2}", focus):
                errors.append(
                    f"{proj.name}: Current focus contains a date; "
                    "narrative belongs in logs/"
                )
            for bullet in map_bullets(focus):
                if normalize(bullet) not in todos_norm:
                    errors.append(
                        f"{proj.name}: Current focus bullet is not verbatim "
                        f"in Active TODOs (paraphrase?): '{bullet}'"
                    )

        state = section(brief, "Current state")
        if state and re.search(r"\bOn \d{4}-\d{2}-\d{2}\b", state):
            errors.append(
                f"{proj.name}: Current state has session narrative "
                "('On YYYY-MM-DD ...'); move it to logs/"
            )

        for m in re.finditer(r"\]\((\.\./\.\./meetings/[^)#]+\.md)\)", brief):
            if not (proj / m.group(1)).resolve().exists():
                errors.append(
                    f"{proj.name}: broken meeting back-link {m.group(1)}"
                )

    if errors:
        print("Convention check FAILED:")
        for e in errors:
            print(f"  - {e}")
        return 1
    print("Convention check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
