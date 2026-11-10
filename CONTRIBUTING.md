# Contributing

## Setup
```sh
brew install lilypond uv
uv sync                 # Python tools + dev dependencies
bin/score               # build PDFs into out/
```

## Workflow
1. **Pick or open an issue.** Assign it to yourself so you don't both work on it.
2. **Branch from `main`:** `git switch -c feat/op9-1-import`.
   Prefixes: `feat/`, `fix/`, `docs/`, `chore/`.
3. **Commit with [Conventional Commits](https://www.conventionalcommits.org):**
   `feat: import Nocturne Op. 9 No. 1`, `fix: pedal bracket overlap in bar 5`.
4. **Open a pull request** with `Closes #<issue>` in the description. Fill in the
   template and add screenshots for anything visual.
5. **CI must pass, and the other person approves.** `main` is protected, so nobody
   pushes to it directly.
6. **Squash-merge** and delete the branch.

Keep PRs small: one piece, one feature, or one style change each.

## Before pushing
```sh
uv run sheetmusic lint      # score rules (see CLAUDE.md)
uv run ruff check . && uv run ruff format --check .
uv run pytest
bin/score
```

## Working with Claude Code
- `CLAUDE.md` holds the project rules, and both of our Claude sessions read it. When
  you correct Claude about something project-specific, add it there in the same PR.
- Claude can write the code, but a human still reviews every PR. Running
  `/code-review` before asking for review catches the easy problems.

## Decisions
Big choices are written up in `docs/decisions/`. Add a new numbered file when you
make one (what we decided, why, and what we gave up).
