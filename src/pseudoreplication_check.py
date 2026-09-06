"""
pseudoreplication_stability_check.py

Extends the single-draw pseudoreplication check (see statistical_analysis.py,
Week 4 in the README) into a REPEATED stability check.

The single-draw version keeps exactly one work per composer, chosen once,
and reports one p-value per feature. That result depends on WHICH work
happened to be kept for every multi-work composer -- a different (equally
valid) choice can give a different p-value. This script instead re-draws
the "one work per composer" selection many times (default 2000) and
reports, for each feature, the FRACTION of draws that reach p < 0.05.
That fraction is a much more honest description of how solid a finding
is than a single p-value from a single arbitrary draw.

Usage:
    python pseudoreplication_stability_check.py path/to/classical_features.csv

Expected CSV columns:
    work_name, composer, style_period,
    pitch_range, harmonic_complexity, rhythmic_variability, note_density

If your current CSV doesn't have a 'composer' column yet, add one --
it's a required input for this check, not optional metadata (the whole
point of the check is testing across composers, not across works).

Dependencies: pandas, numpy, scipy
    pip install pandas numpy scipy
"""

import sys
import numpy as np
import pandas as pd
from scipy import stats

FEATURE_COLUMNS = [
    'pitch_range',
    'harmonic_complexity',
    'rhythmic_variability',
    'note_density',
]


def kruskal_wallis_p(df, feature_col, group_col='style_period'):
    """Kruskal-Wallis p-value for `feature_col` across `group_col` groups."""
    groups = [g[feature_col].dropna().values for _, g in df.groupby(group_col)]
    _, p_value = stats.kruskal(*groups)
    return p_value


def stability_check(df, feature_cols=FEATURE_COLUMNS, group_col='style_period',
                     composer_col='composer', n_draws=2000, alpha=0.05):
    """
    Runs the de-duplication test `n_draws` times, each time keeping a
    different random selection of one work per composer, and reports
    how often each feature reaches significance.

    Returns a DataFrame with, for each feature:
      - pct_significant: fraction of draws with p < alpha
      - median_p: median p-value across all draws (a representative
        single number to quote, less arbitrary than picking one draw)
      - min_p / max_p: the most and least favorable draws found,
        useful for showing the full range rather than just one summary
      - n_composers: number of independent composers in the de-duplicated
        sample (constant across draws, shown for reference)
    """
    n_composers = df[composer_col].nunique()
    p_values = {f: [] for f in feature_cols}

    for seed in range(n_draws):
        deduped = df.groupby(composer_col).sample(n=1, random_state=seed)
        for f in feature_cols:
            p_values[f].append(kruskal_wallis_p(deduped, f, group_col))

    rows = []
    for f in feature_cols:
        arr = np.array(p_values[f])
        rows.append({
            'feature': f,
            'pct_significant': (arr < alpha).mean(),
            'median_p': np.median(arr),
            'min_p': arr.min(),
            'max_p': arr.max(),
            'n_composers': n_composers,
            'n_draws': n_draws,
        })

    return pd.DataFrame(rows).set_index('feature')


def print_report(result):
    """Human-readable summary, formatted for pasting into a brief/paper."""
    print(f"Stability check across {int(result['n_draws'].iloc[0])} random "
          f"de-duplication draws ({int(result['n_composers'].iloc[0])} "
          f"independent composers):\n")
    for feature, row in result.iterrows():
        print(f"  {feature}")
        print(f"    significant in {row['pct_significant']:.1%} of draws")
        print(f"    median p = {row['median_p']:.4f}  "
              f"(range: {row['min_p']:.4f} - {row['max_p']:.4f})")
        print()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python pseudoreplication_stability_check.py "
              "path/to/classical_features.csv")
        sys.exit(1)

    csv_path = sys.argv[1]
    df = pd.read_csv(csv_path)

    required_cols = {'composer', 'style_period', *FEATURE_COLUMNS}
    missing = required_cols - set(df.columns)
    if missing:
        print(f"ERROR: CSV is missing required column(s): {missing}")
        print("A 'composer' column is required -- see the module "
              "docstring for the expected format.")
        sys.exit(1)

    result = stability_check(df)
    print_report(result)
    result.to_csv('stability_check_results.csv')
    print("Full results (including min/max p per feature) written to "
          "stability_check_results.csv")
