# private/

Your own copies of **copyrighted** pieces (purchased sheet music you've typeset,
personal transcriptions), so you can print them in the house style. They never
reach GitHub:

- Everything here except this README is gitignored, and CI fails if any other file
  under `private/` is ever committed.
- `bin/score` builds `private/*.ly` into `out/private/`. `bin/score --share` refuses to
  build them.

Start a file the same way as any score (`\version "2.26.0"`, `\include "house.ily"`).
`sheetmusic lint` doesn't check this folder by default. Run
`uv run sheetmusic lint private/*.ly` if you want the checks.
