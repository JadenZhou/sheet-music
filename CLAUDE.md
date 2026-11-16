# sheet-music

Personal piano sheet music, typeset with LilyPond (think LaTeX for music) in one
consistent house style. Sources are public-domain pieces, mostly from Mutopia.

## Layout
- `style/house.ily` — the house style. Preferences block at the top (fonts, staff
  size, fingering size, pedal style, paper, credits). All look-and-feel lives here.
- `scores/*.ly` — one file per piece: header, macros, music, `\score`. Music only.
- `sources/` — original downloads, kept untouched for reference.
- `bin/score [--share] [files]` — builds PDFs into `out/` (gitignored).
- `reference/` — other editions used as visual references (gitignored; copyrighted).
- `src/sheetmusic/` — Python tooling (uv, ruff, pytest). `uv run sheetmusic lint`
  checks scores against the rules below. When you add a rule here, add it to
  `lint.py` too, if a machine can check it.

## Requirements
LilyPond 2.26 (`brew install lilypond`). Scores start with `\version "2.26.0"`.

## Rules
- **No hand-placed positioning in scores.** No `extra-offset`, hard-coded
  `positions`, or `staff-padding` tweaks for single objects. Old Mutopia sources are
  full of them, tuned for old LilyPond versions, and they break. Strip them when you
  import a piece. Fix layout problems in `house.ily`, or with a small semantic helper
  like `\delayedTurn` in the score.
- **Keep the music semantic.** Use `\sustainOn`/`\sustainOff`, `\tempo "Andante" 8 = 132`,
  `\ottava`, and so on, not markup that only looks like them, so the house style can
  restyle everything.
- **Credits:** Mutopia files are mostly CC BY-SA. Every score header needs `source`
  and `license` fields. Credits print only with `bin/score --share`. Use that for
  anything given to other people.
- **Licenses:** code is MIT (`LICENSE`); scores are CC BY-SA 3.0 (`LICENSE-SCORES`).
  Only import sources whose license allows that: public domain, CC0, CC BY, or CC BY-SA.
  Never NC/ND or unlicensed sources. Note any other license in the score's header and the README table.
- **Never commit** another publisher's edition (PDFs or scans in `reference/`) or
  fingerings copied from a copyrighted edition.

## Importing a new piece from Mutopia
1. Download the `.ly` into `sources/`.
2. Copy it to `scores/<composer>-<piece>.ly` and run `convert-ly -e` on the copy.
3. Replace the Mutopia `\paper`, staff size, `\layout` overrides and tagline with
   `\include "house.ily"` plus a short `\header` (title, opus, composer, dedication,
   source, license).
4. Map the source's custom macros to semantic commands. See `scores/chopin-op9-2.ly`
   for an example.
5. Run `bin/score scores/<file>.ly`, then fix any warnings that matter.

## Checking output
To look at a page, render a PNG:
`lilypond -s -I "$PWD/style" --png -dresolution=110 -o /tmp/x scores/<file>.ly`.
Do this before telling anyone that a layout change works.

## Workflow
Follow `CONTRIBUTING.md`: work on a branch, use Conventional Commits, open a PR that
links its issue, and never push to `main`. Before committing, run
`uv run sheetmusic lint`, `uv run ruff check .`, `uv run ruff format --check .`,
`uv run pytest` and `bin/score`.

## Plans
Work is tracked in GitHub issues and milestones (`gh issue list`). The design behind
features (fingering engine, difficulty levels) is in `ROADMAP.md`. Read the relevant
section before starting feature work, and link the issue in your PR (`Closes #N`).
