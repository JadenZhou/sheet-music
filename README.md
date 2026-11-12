# sheet-music

Piano sheet music, typeset with [LilyPond](https://lilypond.org) in one consistent house style.

## Setup
```sh
brew install lilypond uv
uv sync              # Python tools (score checks, analysis)
bin/score            # builds every score into out/
open out/chopin-op9-2.pdf
```

## Everyday use
| Task | How |
|---|---|
| Build one piece | `bin/score scores/chopin-op9-2.ly` |
| Build a copy to share (includes source/licence credits) | `bin/score --share` |
| Change the look of everything (fonts, size, pedals...) | edit the preferences block at the top of `style/house.ily` |
| Change notes or fingering | edit `scores/<piece>.ly`. A fingering is written `-3` after a note, e.g. `c4-3` |

An editor with live preview helps: [Frescobaldi](https://frescobaldi.org) (free). Clicking a note in the PDF jumps to it in the source.

## Scores
| Piece | Source |
|---|---|
| Chopin, Nocturne Op. 9 No. 2 | Mutopia #1590 (CC BY-SA 3.0) |

How we work together: `CONTRIBUTING.md`. Project rules (also read by Claude Code): `CLAUDE.md`. Planned features: `ROADMAP.md`. Big decisions: `docs/decisions/`.
