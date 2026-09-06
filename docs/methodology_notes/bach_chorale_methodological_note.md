# Methodological Note: Bach Chorales as a Construct-Validity Case Study

*Supplementary cross-genre analysis, separate from the main string-quartet /
four-part-string-texture comparison. Bach chorales are not compared across
style periods here — they are used to test what the "Harmonic Complexity"
metric actually measures.*

## The question

"Harmonic Complexity," as defined in this project, is the mean number of
distinct pitch classes (0–11, octave-independent) per vertical slice after
`chordify()`. Does a high score on this metric mean a passage is
harmonically sophisticated in the way a listener or music theorist would
normally mean that phrase — rich chord vocabulary, functional/tonal
complexity, adventurous dissonance treatment?

## The test

Bach's four-part chorale harmonizations are a natural stress-test: they are
widely taught as an *introductory* model of conventional, diatonic,
functional four-part harmony — the opposite of "harmonically adventurous."
If the metric tracks harmonic sophistication, chorales should score
*low* relative to string quartet movements, especially relative to
20th-century quartets (Debussy, Ravel, Bartók) generally considered far
more harmonically exploratory.

**Method:** rather than relying on the 5 chorales already in the main
corpus (a sample too small, and not necessarily unbiased, to make this
argument on its own), 28 additional four-part chorales were sampled from
music21's built-in Bach corpus (413 chorale files total; every 15th file
taken, to avoid cherry-picking) and the same, already-validated feature
functions were applied.

## Result

| | Harmonic Complexity |
|---|---|
| Broad chorale sample (n=28) | mean 3.267, median 3.273, range 2.96–3.52 |
| Original 5-chorale pilot sample | mean ≈ 3.26 |
| Classical-period quartet movements | 2.43–2.78 |
| Early Romantic quartet movements | 2.57–2.83 |
| Late Romantic / early 20th-c. quartet movements (incl. Debussy, Bartók, Ravel) | 2.70–3.08 |

The broad, unbiased 28-chorale sample confirms the original 5-chorale
finding was not a fluke: **Bach chorales score consistently higher on this
metric than nearly every string quartet movement in the corpus, across all
four style periods** — including the Debussy, Bartók, and Ravel movements,
which are the most harmonically adventurous works in the entire dataset by
any conventional music-historical account.

## Why this happens

The metric is doing exactly what it is defined to do — counting how many
distinct pitch classes sound *at the same instant* — and chorales score
high on that specific, narrow question for a structural reason that has
nothing to do with harmonic sophistication: a four-part chorale is
homophonic. All four voices move together in tight rhythmic lockstep on
nearly every beat, and functional four-part harmony rarely doubles the
same pitch class across all four voices, so nearly every vertical slice
contains close to four distinct pitch classes.

A string quartet's texture is far less consistently homophonic — passages
of solo melody over accompaniment, unison writing, rests in individual
parts, and imitative counterpoint all produce moments where fewer than
four distinct pitch classes sound at once, pulling the *average* down —
even in a passage that a listener would readily call harmonically richer
or more adventurous than a chorale.

## Conclusion for the main study

"Harmonic Complexity" as defined here should be reported and discussed as
a measure of **vertical pitch-class density** (how tightly the texture
packs simultaneous, distinct pitches), not of harmonic sophistication in
the colloquial or music-theoretic sense (chord vocabulary, tonal distance,
dissonance treatment, functional progression). This is a limitation of the
metric's name, not of the underlying computation, and should be stated
explicitly wherever the feature is introduced in the main paper — the
Bach chorale result above is the cleanest available demonstration of why
that caveat matters.
