from pathlib import Path

from sheetmusic.lint import lint_paths, lint_text, strip_comment

GOOD = r"""\version "2.26.0"
\include "house.ily"
\header {
  title   = "Test"
  source  = "Mutopia #1"
  license = "CC BY-SA 3.0"
}
upper = \relative c'' { c4-1 d-2 e-3 f-4 }
"""


def lint(text):
    return lint_text(text, Path("x.ly"))


def test_good_score_passes():
    assert lint(GOOD) == []


def test_extra_offset_is_flagged_with_line_number():
    text = GOOD + "\\once \\override TextScript.extra-offset = #'(1 . 2)\n"
    [problem] = lint(text)
    assert problem.line == GOOD.count("\n") + 1
    assert "extra-offset" in problem.message


def test_hard_coded_slur_positions_are_flagged():
    [problem] = lint(GOOD + "\\once \\override Slur.positions = #'(1 . 2)\n")
    assert "positions" in problem.message


def test_banned_pattern_in_comment_is_ignored():
    assert lint(GOOD + "% removed the extra-offset tweaks here\n") == []


def test_percent_inside_string_is_not_a_comment():
    assert strip_comment('x = "50% off" % note') == 'x = "50% off" '


def test_missing_credits_are_flagged():
    text = GOOD.replace('  source  = "Mutopia #1"\n', "").replace(
        '  license = "CC BY-SA 3.0"\n', ""
    )
    messages = [p.message for p in lint(text)]
    assert any("source" in m for m in messages)
    assert any("license" in m for m in messages)


def test_wrong_version_and_missing_house_style_are_flagged():
    text = GOOD.replace("2.26.0", "2.12.2").replace('\\include "house.ily"\n', "")
    messages = [p.message for p in lint(text)]
    assert any("version" in m for m in messages)
    assert any("house.ily" in m for m in messages)


def test_real_scores_pass():
    scores = sorted(Path(__file__).parent.parent.glob("scores/*.ly"))
    assert scores, "no scores found"
    assert lint_paths(scores) == []
