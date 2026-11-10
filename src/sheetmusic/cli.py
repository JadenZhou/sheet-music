import argparse
import sys
from pathlib import Path

from sheetmusic.lint import lint_paths


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="sheetmusic")
    commands = parser.add_subparsers(dest="command", required=True)

    lint = commands.add_parser("lint", help="check scores against the project rules")
    lint.add_argument("files", nargs="*", type=Path, help="default: scores/*.ly")

    args = parser.parse_args(argv)

    if args.command == "lint":
        files = args.files or sorted(Path("scores").glob("*.ly"))
        problems = lint_paths(files)
        for problem in problems:
            print(problem)
        print(f"{len(files)} score(s) checked, {len(problems)} problem(s)")
        return 1 if problems else 0
    return 2


if __name__ == "__main__":
    sys.exit(main())
