# 001: LilyPond text files are the source of truth

**Status:** accepted (2026-10-10)

## Decision
Every piece lives in `scores/*.ly` as LilyPond source. PDFs are build output and are
not committed. All visual choices live in `style/house.ily`.

## Why
- Plain text: diffs, code review and merging work like they do for code.
- A shared style file gives every score the same look, like a LaTeX preamble.
- Free, scriptable, and high-quality engraving. Mutopia already offers hundreds of
  public-domain pieces in this format.

## Trade-offs
- Harder to analyse with code than MusicXML. For analysis (difficulty, fingering),
  read LilyPond's MIDI output, or convert to MusicXML when needed (see 002).
- Old Mutopia sources need cleanup (hand-placed offsets) when imported.

## Alternatives considered
- MuseScore / MusicXML as the source: friendlier GUI, but XML diffs are unreadable
  and the look is harder to standardise.
- Sibelius / Dorico: commercial, binary files.
