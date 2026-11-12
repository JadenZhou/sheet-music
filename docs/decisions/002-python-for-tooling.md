# 002: Python for analysis and tooling

**Status:** accepted (2026-11-10)

## Decision
Tooling beyond typesetting (score checks, difficulty analysis, fingering, OMR glue)
is a Python package in `src/sheetmusic/`, managed with uv and checked with ruff and
pytest. Engraving stays in LilyPond, and simple music transformations (e.g.
removing ornaments) may be LilyPond Scheme functions in the house style.

## Why
- Symbolic music libraries live in Python: music21, mido/pretty_midi, partitura.
- The fingering and difficulty research (PIG dataset, published models) uses Python,
  as does the ML stack (numpy, PyTorch) if we train anything.
- OMR tools (Audiveris, oemer) are easiest to script from Python.

## Trade-offs
- Two languages: Scheme inside LilyPond for in-score transformations, Python outside.
  Rule of thumb: if it changes how a score *prints*, use Scheme/LilyPond. If it
  *analyses* or *generates* music, use Python.
- `bin/score` stays a small shell script until it needs more than it does now.
