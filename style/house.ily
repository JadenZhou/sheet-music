%% house.ily — personal house style for piano scores.
%% Include at the top of every score:  \include "house.ily"
%% Change the preferences block, recompile, and every score follows.
%% A score can override any preference by setting it *before* the include.

\version "2.26.0"

#(define (pref sym default)
   (let ((v (ly:parser-lookup sym))) (if (null? v) default v)))

%% ---------------------------------------------------------------
%% Preferences
%% ---------------------------------------------------------------
% music glyphs (notes, clefs...): emmentaler (LilyPond default). Others
%   (gutenberg1939, beethoven, haydn...) are free from github.com/OpenLilyPondFonts
%   and must be copied into LilyPond's fonts/otf folder first.
musicFont     = #(pref 'musicFont "emmentaler")
% text (title, expression marks): any installed font, e.g. "Baskerville",
%   "Big Caslon", "Hoefler Text", "Palatino", "C059" (LilyPond default)
textFont      = #(pref 'textFont "C059")
% fingering numbers: 'text (light serif, like Sibelius/Henle) or 'music (bold)
fingeringFont = #(pref 'fingeringFont 'text)
staffSize     = #(pref 'staffSize 18)        % default 20; print editions ~17-20
fingeringSize = #(pref 'fingeringSize -3)    % font-size step
pedalStyle    = #(pref 'pedalStyle 'bracket) % 'text ("Ped. *"), 'bracket, 'mixed
paperSize     = #(pref 'paperSize "letter")
% source/licence line at the end: off for personal prints,
% on with `bin/score --share` (CC BY-SA sources require it when shared)
showCredits   = #(pref 'showCredits (and (getenv "SHOW_CREDITS") #t))

#(set-global-staff-size staffSize)

% \finger "54" text annotations follow the same fingering font as real fingerings
#(if (eq? fingeringFont 'text)
  (define-markup-command (finger layout props arg) (markup?)
    (interpret-markup layout props
      (make-fontsize-markup (- fingeringSize 1) arg))))

%% ---------------------------------------------------------------
%% Page
%% ---------------------------------------------------------------
\paper {
  #(set-paper-size paperSize)
  property-defaults.fonts.music = \musicFont
  property-defaults.fonts.serif = \textFont

  top-margin    = 12\mm
  bottom-margin = 12\mm
  left-margin   = 15\mm
  right-margin  = 15\mm

  % roomy, even spacing between systems; fill pages to the bottom
  system-system-spacing = #'((basic-distance . 14) (minimum-distance . 10)
                             (padding . 2) (stretchability . 60))
  markup-system-spacing = #'((basic-distance . 8) (padding . 2))
  ragged-last-bottom = ##f

  % title block: dedication, large regular-weight title centred,
  % composer and opus at the right
  bookTitleMarkup = \markup \column {
    \fill-line { \italic \fromproperty #'header:dedication }
    \overlay {
      \fill-line { \fontsize #9 \fromproperty #'header:title }
      \fill-line { "" \right-column {
        \fromproperty #'header:composer
        \fromproperty #'header:opus } }
    }
    \vspace #1
  }
  scoreTitleMarkup = ##f

  % page numbers bottom-centre, not on page 1
  print-first-page-number = ##f
  oddHeaderMarkup  = \markup ""
  evenHeaderMarkup = \markup ""
  oddFooterMarkup  = \markup \column {
    \fill-line { \if \should-print-page-number \fromproperty #'page:page-number-string }
    \fill-line { \if \on-last-page-of-part \fromproperty #'header:tagline }
  }
  evenFooterMarkup = \oddFooterMarkup

  % small source/licence credit at the end (see showCredits)
  tagline = #(and showCredits
    #{ \markup \small \with-color #(rgb-color 0.45 0.45 0.45) \line {
         \fromproperty #'header:source " · " \fromproperty #'header:license } #})
}

%% ---------------------------------------------------------------
%% Engraving
%% ---------------------------------------------------------------
\layout {
  % no first-line indent (it exists to fit an instrument name, which we hide)
  indent = 0
  short-indent = 0
  \context {
    \Score
    % bar number at the start of every system, a bit larger than default
    \override BarNumber.font-size = #-1
    \override BarNumber.padding = #1.5
    % tighter horizontal spacing (default 0.6): more bars per line, fewer page turns
    \override SpacingSpanner.spacing-increment = #0.5
  }
  \context {
    \PianoStaff
    % solo piano: no "Piano" label in front of the first system
    instrumentName = ##f
    shortInstrumentName = ##f
  }
  \context {
    \Voice
    \override Fingering.font-size = \fingeringSize
    \override Fingering.avoid-slur = #'inside
    \override Fingering.font-encoding =
      #(if (eq? fingeringFont 'text) 'latin1 'fetaText)
  }
  \context {
    \Staff
    pedalSustainStyle = \pedalStyle
    % hang all pedal brackets of a system from one baseline
    \override SustainPedalLineSpanner.staff-padding = #4
  }
}
