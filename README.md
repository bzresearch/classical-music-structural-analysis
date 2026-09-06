# Structural Feature Trends in Western Classical Music

Research repository for an independent project testing whether structural
features of classical music (pitch range, harmonic complexity, rhythmic
variability, note density) show cyclical or monotonic trends across style
periods, using symbolic score data.

## Key methodological findings (self-correction arc)

Three independent findings, each caught and corrected during the project
itself rather than assumed correct from the start. Full details and
exact dates/numbers are in `CHANGELOG.md`; this is the one-line version:

1. **Pseudoreplication.** A naive test found 3 of 4 features significant
   across style periods -- but two of the four groups were dominated by
   a single composer (Bach, Beethoven), so the "era effect" could really
   have been a "this one composer's style" effect. Re-tested with one
   work per composer; only pitch range survived.
2. **Analysis-unit inconsistency.** Some works in the corpus were single
   movements, others were complete multi-movement files (66 vs. 882
   measures for two pieces) -- discovered this was silently inflating
   later-period feature values. Standardized on averaging across all
   movements per work, and re-ran everything.
3. **Metric validity check.** Used an unbiased 28-chorale sample to test
   whether "Harmonic Complexity" measures what its name suggests. It
   doesn't -- it measures vertical pitch-class density, which is why
   homophonic Bach chorales score *higher* than harmonically adventurous
   20th-century quartets. See `docs/methodology_notes/`.

## Repository structure

```
data/
  raw_scores/           # original score files, never modified after adding
    baroque/<composer>/
    classical/<composer>/
    romantic_early/<composer>/
    romantic_late/<composer>/
  MANIFEST.md           # source + provenance + editor/copyright for every file in raw_scores/
  processed/            # extracted feature CSVs -- see naming convention below

src/
  feature_extraction.py     # the 4 feature functions + batch driver
  statistical_analysis.py   # Kruskal-Wallis / Mann-Kendall / bootstrap
  movement_utils.py         # movement-splitting / averaging helpers
  pseudoreplication_check.py # exhaustive + random-draw stability check

docs/
  methodology_notes/    # standalone write-ups of methodology decisions/findings
  briefs/               # the outreach brief (English + Chinese), dated versions
  outreach_log/         # who was contacted, when, about what, response status
  candidate_works_tracker.md   # works found but not yet processed into the corpus

CHANGELOG.md             # dated log -- update this every session, see below
```

## Naming convention for `data/processed/`

Never overwrite a results CSV. Each time the corpus or a feature definition
changes, save a NEW dated file:

```
classical_features_2026-08-24.csv   (25 works, pre-Mendelssohn)
classical_features_2026-08-26.csv   (26 works, movement-1-only)
classical_features_2026-09-02.csv   (26 works, all-movements-averaged)
classical_features_2026-09-05.csv   (27 works, +Fasch)
```

This is not clutter -- being able to show "here is exactly what changed and
when, and here is the effect on the result" is itself part of the
methodology story (see `docs/methodology_notes/`).

## Weekly update routine

Do this at the end of any work session, not necessarily on a fixed day:

1. **New score files found/verified this session?**
   → Add the raw file(s) to `data/raw_scores/<period>/<composer>/`.
   → Add one row per file to `data/MANIFEST.md` (source, editor/arranger,
     license, instrumentation notes).
   → If not yet processed into features, add/update its entry in
     `docs/candidate_works_tracker.md` instead of `MANIFEST.md`.

2. **Code changed (new feature, bug fix, new analysis)?**
   → Commit directly to the relevant file in `src/`.
   → Write the commit message as what changed AND why (e.g. "Fix
     get_note_density double-counting measures across parts (105→21 for
     bwv1.6)") -- this commit history is itself evidence of real,
     independent debugging work.

3. **Corpus composition or a feature definition changed?**
   → Re-run the pipeline, save a new dated CSV to `data/processed/`
     (never overwrite the old one).
   → Add one line to `CHANGELOG.md`: what changed, old result → new result.

4. **New methodological finding or decision (e.g. a case study, a
   limitation discovered, a convention adopted)?**
   → Add a new file to `docs/methodology_notes/`, or append to an
     existing one if it's a direct continuation.

5. **Contacted anyone, or got a reply?**
   → Log it in `docs/outreach_log/` (see template there). Keep the
     actual email text out of the public repo if the project is ever
     made public -- log the fact and substance of the exchange, not the
     verbatim personal correspondence.

6. **Brief needs updating for outreach?**
   → Save the new version into `docs/briefs/` with a date in the
     filename; don't overwrite the previous version.

## Current status

See `CHANGELOG.md` for the dated history. Quick summary as of the last
entry: 27 works, 13 independent composers, pitch range is the one feature
confirmed robust across rigorous testing (see
`docs/methodology_notes/` for the full pseudoreplication and
movement-consistency story).
