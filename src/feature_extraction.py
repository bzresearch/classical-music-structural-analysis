"""
feature_extraction.py

Computes four structural features from a symbolic music score
(MusicXML or MIDI, anything music21 can parse) using a single, uniform
definition per feature so results are comparable across works, composers,
and style periods.

Dependencies: music21, pandas
    pip install music21 pandas --break-system-packages
"""

import statistics
import music21 as m21
import pandas as pd


def get_pitch_range(score):
    """Semitone span between the highest and lowest pitch in the piece."""
    midi_pitches = []
    for element in score.recurse().notes:
        if element.isNote:
            midi_pitches.append(element.pitch.midi)
        elif element.isChord:
            midi_pitches.extend(p.midi for p in element.pitches)
    if not midi_pitches:
        return None
    return max(midi_pitches) - min(midi_pitches)


def get_harmonic_complexity(score):
    """
    Mean number of distinct pitch classes (0-11) per vertical slice after
    chordify(). Measures vertical pitch-class DENSITY, not functional
    harmony/dissonance/tonal distance -- see
    docs/methodology_notes/bach_chorale_case_study.md for why this
    distinction matters. Only meaningful for genuine multi-voice texture;
    not computable for a monophonic melody (e.g. BiMMuDa pop-side data).
    """
    chordified = score.chordify()
    pitch_class_counts = []
    for element in chordified.recurse().notes:
        if element.isChord:
            pitch_class_counts.append(len({p.pitchClass for p in element.pitches}))
        elif element.isNote:
            pitch_class_counts.append(1)
    if not pitch_class_counts:
        return None
    return sum(pitch_class_counts) / len(pitch_class_counts)


def get_rhythmic_variability(score):
    """Coefficient of variation (CoV) of note durations (quarterLength)."""
    durations = [n.quarterLength for n in score.recurse().notes if n.quarterLength > 0]
    if len(durations) < 2:
        return None
    mean_duration = statistics.mean(durations)
    if mean_duration == 0:
        return None
    return statistics.stdev(durations) / mean_duration


def get_note_density(score):
    """
    Note/Chord events per measure. A chord counts as ONE event.

    IMPORTANT: count measures from a SINGLE representative part
    (score.parts[0]), not from score.recurse() -- a multi-part score has
    one Measure object per part per bar, so recursing over the whole
    score inflates the measure count by a factor equal to the part count
    and silently makes density ~N-parts times too low. Verified against
    bach/bwv1.6: 105 "measures" via naive recurse vs. 21 real bars.
    """
    events = list(score.recurse().notes)
    if score.parts:
        n_measures = len(score.parts[0].getElementsByClass('Measure'))
    else:
        n_measures = len(score.getElementsByClass('Measure'))
    if n_measures == 0:
        return None
    return len(events) / n_measures


def extract_all_features(filepath, work_name, style_period, composer):
    """Parse a single score file and extract all four structural features."""
    score = m21.converter.parse(filepath)
    return {
        'work_name': work_name,
        'composer': composer,
        'style_period': style_period,
        'pitch_range': get_pitch_range(score),
        'harmonic_complexity': get_harmonic_complexity(score),
        'rhythmic_variability': get_rhythmic_variability(score),
        'note_density': get_note_density(score),
    }


def build_corpus_dataframe(work_list):
    """
    work_list: list of dicts, each with keys
        'filepath', 'work_name', 'style_period', 'composer'
    """
    rows = []
    for work in work_list:
        print(f"  Processing: {work['work_name']} ...")
        try:
            rows.append(extract_all_features(
                work['filepath'], work['work_name'],
                work['style_period'], work['composer'],
            ))
        except Exception as e:
            print(f"    FAILED: {work['work_name']} -- {e}")
    return pd.DataFrame(rows)
