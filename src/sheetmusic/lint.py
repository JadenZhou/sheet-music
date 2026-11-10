"""Check scores against the project rules in CLAUDE.md.

Rules:
- no hand-placed positioning (extra-offset, hard-coded positions)
- every score pins the LilyPond version and includes the house style
- every score header credits its source and licence
"""

import re
from dataclasses import dataclass
from pathlib import Path

LILYPOND_VERSION = "2.26.0"

# (pattern, message) pairs checked line by line, ignoring % comments
BANNED = [
    (re.compile(r"extra-offset"), "hand-placed extra-offset; let the house style position it"),
    (
        re.compile(r"\.positions\s*=\s*#'\("),
        "hard-coded slur/beam positions; let LilyPond place it",
    ),
]

REQUIRED = [
    (
        re.compile(r'\\version\s+"' + re.escape(LILYPOND_VERSION) + '"'),
        f'missing \\version "{LILYPOND_VERSION}"',
    ),
    (re.compile(r'\\include\s+"house\.ily"'), 'missing \\include "house.ily"'),
    (re.compile(r"^\s*source\s*=", re.M), "header has no source = ... credit"),
    (re.compile(r"^\s*license\s*=", re.M), "header has no license = ... field"),
]


@dataclass(frozen=True)
class Problem:
    path: Path
    line: int  # 1-based; 0 means the whole file
    message: str

    def __str__(self) -> str:
        where = f"{self.path}:{self.line}" if self.line else str(self.path)
        return f"{where}: {self.message}"


def strip_comment(line: str) -> str:
    """Drop a LilyPond % comment (not inside a string)."""
    in_string = False
    for i, ch in enumerate(line):
        if ch == '"' and (i == 0 or line[i - 1] != "\\"):
            in_string = not in_string
        elif ch == "%" and not in_string:
            return line[:i]
    return line


def lint_text(text: str, path: Path) -> list[Problem]:
    problems = []
    code_lines = [strip_comment(line) for line in text.splitlines()]
    for number, line in enumerate(code_lines, start=1):
        for pattern, message in BANNED:
            if pattern.search(line):
                problems.append(Problem(path, number, message))
    code = "\n".join(code_lines)
    for pattern, message in REQUIRED:
        if not pattern.search(code):
            problems.append(Problem(path, 0, message))
    return problems


def lint_paths(paths: list[Path]) -> list[Problem]:
    problems = []
    for path in paths:
        problems.extend(lint_text(path.read_text(encoding="utf-8"), path))
    return problems
