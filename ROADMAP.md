# Roadmap

The **design** behind planned features. **Tracking** (who's doing what, status) lives
in GitHub issues and milestones; each section here has matching issues. When something
ships, close its issue and move it to Done below.

## Done
- House style (`style/house.ily`): fonts, spacing, bracket pedals, light fingerings,
  no first-line indent, credits only with `bin/score --share`.
- Chopin Nocturne Op. 9 No. 2, imported from Mutopia and cleaned up.

## Next
- Import Nocturne Op. 9 No. 1 (#2)
- Kravchuk-style pedalling: one continuous line with a notch at each change (#3)
- Scan → score with OMR (Audiveris → MusicXML → `musicxml2ly`) (#10)

## Fingering engine
Suggest fingerings automatically, personalised to the player's hand size and habits.
- Prior work: Parncutt et al. 1997 (scoring fingerings by how hard they are on the
  hand), dynamic-programming search, Nakamura et al. 2020 + the PIG dataset of
  pianist-fingered pieces, the open-source `pianoplayer`.
- Output is just LilyPond fingering (`c4-3`), so it plugs into the existing scores.
- A fingering's cost is also a difficulty measure (see below).

## Difficulty levels
Two halves: measure difficulty, then reduce it.

### 1. Measuring (per bar)
| Feature | Op. 9 No. 2 example |
|---|---|
| Notes per second | bar 32 cadenza |
| Hand stretch: widest chord in one hand | LH 10ths |
| Leaps: distance × speed of jumps | LH bass → chord, every beat |
| Notes played at once in one hand | RH chords, bars 11–12 |
| Independent voices within a hand | melody + inner line in RH |
| Rhythmic complexity | irregular groupings, bars 16 and 24 |
| Ornaments | trills, turns, grace notes |
| Fingering cost | best fingering is still awkward → hard |

- Overall rating = the hardest stretches (e.g. 90th-percentile bar), **not** the
  average. One brutal passage makes a piece hard.
- Calibrate against rated datasets (Henle's 1–9 levels; Ramoneda et al. on predicting
  difficulty from scores).
- Extra: a **per-bar heat map** printed on the score, showing where to practise.
- Features can be computed from the MIDI LilyPond already writes (Python + music21).

### 2. Reducing (simplification moves, least damage first)
1. Drop ornaments (trill → held note, remove grace notes and turns).
2. Thin chords: drop octave doublings, then inner notes. Keep melody (top) and
   bass (bottom); keep root and third before the fifth.
3. Fix stretches: roll or trim chords wider than the target hand size.
4. Shrink leaps: move LH chords closer to the bass note.
5. Simplify runs: shorten cadenzas to scale fragments, straighten irregular rhythms.
6. Simplify accompaniment patterns: arpeggios → block chords on the beat.
7. (Optional) transpose to a key with fewer black keys.

**Algorithm:** pick a target level. Repeatedly take the hardest bar and apply the
cheapest move that brings it under the target, until every bar fits.
**The melody must always survive.**

### 3. In LilyPond
- Mechanical moves (1–3) are Scheme filters in the house style, applied to every score.
- Judgment calls (5–6, cadenzas) are hand-written alternatives using tags:
  `\tag #'full { ... } \tag #'easy { ... }`. Claude drafts them, a human checks them
  at the piano.
- Build with something like `bin/score --level easy`.

### First milestone
Difficulty scorer + per-bar heat map for Op. 9 No. 2, then a three-level edition:
original / intermediate (no ornaments, short cadenza) / easy (melody + block chords).

## Other "good sheet music" ideas
- Page turns placed where a hand is free.
- Layouts for each device (print, iPad portrait, two-page spread).
- Composer markings vs editorial markings shown differently (e.g. editorial in grey).
- Pedal suggestions from the harmony.
