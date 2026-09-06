# Changelog

Dated log of what changed and why. Newest entries at the top. This file is
the fastest way for anyone (including future-you) to see the project's
real arc without re-reading every commit.

Format for each entry:
```
## YYYY-MM-DD
- What changed
- Why
- Effect on results, if any (old value → new value)
```

---

## 2026-09-05
- Added Fasch, Ouverture-Suite in G, FaWV K:G15 (Bourrée movement) as a
  third independent Baroque composer, using the 4 core string parts only
  (Violin I/II, Viola, Double Bass; oboes/bassoon/continuo-realization
  excluded per the established 4-part-only rule).
- Corpus: 26 → 27 works, 12 → 13 independent composers.
- Effect: pitch range exhaustive stability check jumped from 41.07% to
  96.43% of all composer-combinations reaching significance. Flagged as a
  genuine result but also a sign of how sensitive small-N combinatorics
  are to a single additional point -- not to be over-claimed as final.

## 2026-09-02 (approx.)
- Switched from "movement 1 only" to "all movements averaged per work" as
  the primary corpus convention, after auditing analysis-unit consistency
  and finding some works used single movements and others used complete
  multi-movement files interchangeably.
- Re-extracted features for all multi-movement works accordingly.
- Effect: pitch range stability (exhaustive) moved from 5.0%
  (movement-1-only) to 41.07% (all-movements-averaged). Documented all
  three versions (mixed/movement-1/averaged) rather than quietly
  replacing one with another, since the swing itself is informative.

## 2026-08-31 (approx.)
- Audited movement/measure consistency across the corpus. Found that
  `get_note_density` was double(+)-counting measures in multi-part
  scores (105 "measures" via naive recurse vs. 21 real bars for
  bach/bwv1.6) -- fixed by counting from a single representative part.
- Found the corpus mixed single-movement and complete-multi-movement
  files for different works (e.g. Haydn single movements vs. Brahms
  full 4-movement file, 66 vs. 882 measures) -- this is a real
  confound, not just a data-hygiene issue; documented and corrected.

## 2026-09-04 (approx.)
- Methodological case study: tested what "Harmonic Complexity" (mean
  distinct pitch classes per vertical slice) actually measures, using an
  unbiased 28-chorale sample from Bach's ~413 four-part chorales (every
  15th file, not cherry-picked). Found Bach chorales score consistently
  *higher* on this metric (mean 3.267) than nearly every string quartet
  movement in the corpus, including Debussy/Bartók/Ravel -- the most
  harmonically adventurous works in the dataset by any conventional
  account. Confirms the metric measures vertical pitch-class density
  (homophonic 4-voice chorales pack more simultaneous distinct pitches
  than quartet textures with solo lines, unisons, and rests), not
  harmonic sophistication in the colloquial/music-theoretic sense. Full
  write-up: `docs/methodology_notes/bach_chorale_methodological_note.md`.

## 2026-08-27 (approx.)
- Pseudoreplication check: naive Kruskal-Wallis found 3/4 features
  significant, but 2 of 4 style-period groups were dominated by a single
  composer (Bach 5/6 Baroque works, Beethoven 5/6 original Early
  Romantic works). Re-ran with one work per composer kept -- only pitch
  range survived (0.0007 → 0.0399 naive vs. de-duplicated).
- Added Mendelssohn (String Quartet No.2, Op.13) specifically to dilute
  the Beethoven-dominance in the Early Romantic group.
- Replaced single-draw de-duplication with a repeated/exhaustive check
  (see `src/pseudoreplication_check.py`) after realizing a single
  arbitrary draw isn't a reliable summary at this sample size.

## 2026-08-24 (approx.)
- Initial 25-work pilot assembled from music21's built-in corpus (Bach,
  Corelli, Haydn, Mozart, Beethoven, Schumann) and the OpenScore String
  Quartets project (Debussy, Brahms, Ravel, Dvořák, Bartók).
- Corpus and method described in the first pilot brief.
