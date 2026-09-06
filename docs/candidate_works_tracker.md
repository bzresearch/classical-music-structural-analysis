# Candidate Works Tracker

Works identified as matching the "2 violins, viola, bass/continuo"
instrumentation (per Prof. Dirst's suggestion), tracked from discovery
through to actually being processed into `data/processed/`. A work only
moves to `data/MANIFEST.md` once it has real extracted feature values.

Status values: `found` → `instrumentation confirmed` → `usable format
found` → `processed into corpus`

| Composer | Work | Status | Notes |
|---|---|---|---|
| Fasch, J.F. | Ouverture-Suite in G, FaWV K:G15 (Bourrée mvt.) | **processed into corpus** | Native MusicXML found (Michrond ZIP), 4 core string parts extracted. In `data/processed/` as of 2026-09-05. |
| Fasch, J.F. | Ouverture-Suite, FaWV K:G16 | found | User found a second Rondeau-edited piece with likely companion ZIP; not yet confirmed/downloaded. |
| Fasch, J.F. | (untitled) Gavotte (No.3) | found | Unclear yet whether this is a movement of K:G15/K:G16 or a separate work -- needs the actual ZIP to determine. |
| Fasch, J.F. | Sonata for 2 Violins, Viola and Continuo, FaWV N:d3 | instrumentation confirmed | PDF scan only (Boccaccio 2012 / Fynnjamin 2009) -- no native file found. |
| Fasch, J.F. | Sonata for 2 Violins, Viola and Continuo, FaWV N:c1 | instrumentation confirmed | Same as above, PDF scan only. |
| Purcell, H. | Chacony in G minor, Z.730 | usable format found | Clean typeset PDF (R.D. Tennent, 2012), instrumentation visually confirmed (Vln1/Vln2/Vla/basso). No native XML found -- needs OMR or manual entry. |
| Krause, C.G. | Sonata for 2 Violins, Viola and Continuo in F minor | instrumentation confirmed | Confirmed via IMSLP category listing; not yet downloaded/opened. |
| Pasquali, N. | 12 Sonatas for 2 Violins, Viola and Continuo | instrumentation confirmed | Whole 12-work collection; not yet downloaded/opened. |
| Handel, G.F. | Concerto a quattro in D major | instrumentation confirmed | PDF scan only. |
| Handel, G.F. | Quadro Sonata in B-flat major | found | Not yet checked. |
| Telemann, G.P. | Sonata in D major, TWV 44:1 | instrumentation uncertain | May actually be a 5-part "quintet" (with trumpet) per IMSLP discussion page, not a clean 4-part work -- verify before using. PDF scan + MIDI only, no native file. |
| Vivaldi, A. | Sinfonia in G major, RV 149 | found | Not yet checked. |
| Vivaldi, A. | Sonata in E-flat major, RV 130 | found | Not yet checked. |
| Corelli, A. | Sonata a Quattro in G minor, WoO 2 | found | Potentially a cleaner alternative/addition to the Op.3 No.1 trio sonata currently in the corpus (Op.3 No.1 may lack an independent viola part). Not yet checked. |

## Known blocker

OMR (optical music recognition) is currently non-functional in the main
working environment (oemer: onnxruntime/model incompatibility, made worse
by a version-downgrade attempt; Audiveris: blocked by a GitHub API rate
limit on first install attempt). Works whose only available format is a
PDF scan or clean typeset PDF (no native MusicXML/Finale/Sibelius file)
are stuck at "usable format found" until either this is resolved in a
fresh environment, or a native source file is located directly (as
happened for the Fasch K:G15 case, via Michrond's companion ZIP upload).
