import music21 as m21
import statistics
import numpy as np

def get_pitch_range(score):
    midi_pitches = []
    for element in score.recurse().notes:
        if element.isNote:
            midi_pitches.append(element.pitch.midi)
        elif element.isChord:
            midi_pitches.extend(p.midi for p in element.pitches)
    return max(midi_pitches) - min(midi_pitches) if midi_pitches else None

def get_harmonic_complexity(score):
    chordified = score.chordify()
    counts = []
    for element in chordified.recurse().notes:
        if element.isChord:
            counts.append(len({p.pitchClass for p in element.pitches}))
        elif element.isNote:
            counts.append(1)
    return sum(counts)/len(counts) if counts else None

def get_rhythmic_variability(score):
    durations = [n.quarterLength for n in score.recurse().notes if n.quarterLength > 0]
    if len(durations) < 2:
        return None
    mean_d = statistics.mean(durations)
    return statistics.stdev(durations)/mean_d if mean_d else None

def get_note_density(score):
    events = list(score.recurse().notes)
    n_measures = len(score.parts[0].getElementsByClass('Measure'))
    return len(events)/n_measures if n_measures else None

def features_of(score):
    return {
        'pitch_range': get_pitch_range(score),
        'harmonic_complexity': get_harmonic_complexity(score),
        'rhythmic_variability': get_rhythmic_variability(score),
        'note_density': get_note_density(score),
    }

def average_features(list_of_feature_dicts):
    keys = list_of_feature_dicts[0].keys()
    return {k: float(np.mean([d[k] for d in list_of_feature_dicts])) for k in keys}

def split_by_movement_markers(score):
    """Split an OpenScore file into all its movements using the I./II./III./IV./V.
    text markers. Returns a list of sliced Score objects, one per movement."""
    measures0 = list(score.parts[0].getElementsByClass('Measure'))
    boundaries = []
    import re
    marker_pattern = re.compile(r'^(I|II|III|IV|V|VI)\.\s*')
    for idx, m in enumerate(measures0):
        for te in m.recurse().getElementsByClass('TextExpression'):
            if marker_pattern.match(te.content.strip()):
                boundaries.append(idx)
    boundaries = sorted(set(boundaries))
    boundaries.append(len(measures0))  # end of piece

    movements = []
    for i in range(len(boundaries) - 1):
        start, end = boundaries[i], boundaries[i+1]
        new_score = m21.stream.Score()
        for part in score.parts:
            measures = list(part.getElementsByClass('Measure'))
            new_part = m21.stream.Part()
            for m in measures[start:end]:
                new_part.append(m)
            new_score.append(new_part)
        movements.append(new_score)
    return movements

def average_over_movement_files(paths):
    """For music21-corpus works already split into separate movementN.mxl files."""
    feats = []
    for p in paths:
        score = m21.corpus.parse(p) if not p.startswith('/') else m21.converter.parse(p)
        feats.append(features_of(score))
    return average_features(feats), len(paths)

def average_over_openscore_file(path):
    score = m21.converter.parse(path)
    movements = split_by_movement_markers(score)
    if len(movements) <= 1:
        return features_of(score), 1
    feats = [features_of(mv) for mv in movements]
    return average_features(feats), len(feats)
