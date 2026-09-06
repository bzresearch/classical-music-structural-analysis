"""
statistical_analysis.py

Statistical tests for comparing structural features across style-period
groups, chosen for a SMALL-SAMPLE setting (5-8 works per group). Classic
time-series methods (autocorrelation, Fourier analysis, formal
changepoint detection) assume far more data points than this corpus can
provide and are deliberately not used.

Dependencies: pandas, numpy, scipy, pymannkendall
    pip install pandas numpy scipy pymannkendall --break-system-packages
"""

import numpy as np
import pandas as pd
from scipy import stats
import pymannkendall as mk


def run_kruskal_wallis(df, feature_col, group_col='style_period'):
    """Non-parametric one-way ANOVA analogue. Returns (H statistic, p-value)."""
    groups = [g[feature_col].dropna().values for _, g in df.groupby(group_col)]
    return stats.kruskal(*groups)


def run_mann_kendall(df, feature_col, order_col='composition_year'):
    """Tests for a monotonic trend over time without assuming linearity."""
    ordered = df.sort_values(order_col)
    return mk.original_test(ordered[feature_col].dropna().values)


def bootstrap_ci(values, n_iterations=10000, ci=0.95, random_state=None):
    """Bootstrap resampling CI for the mean. Returns (lower, upper)."""
    rng = np.random.default_rng(random_state)
    values = np.asarray(values)
    boot_means = np.empty(n_iterations)
    for i in range(n_iterations):
        boot_means[i] = rng.choice(values, size=len(values), replace=True).mean()
    alpha = 1 - ci
    return (np.percentile(boot_means, 100 * alpha / 2),
            np.percentile(boot_means, 100 * (1 - alpha / 2)))


def deduplicate_by_composer(df, composer_col='composer', random_state=42):
    """
    PSEUDOREPLICATION CHECK -- see CHANGELOG.md 2026-08-27 and
    docs/methodology_notes/. Keeps exactly one (randomly chosen) work per
    composer, since works by the same composer aren't independent
    observations with respect to an era-level question.
    """
    return df.groupby(composer_col).sample(n=1, random_state=random_state)


def pseudoreplication_check(df, feature_cols, group_col='style_period',
                              composer_col='composer', random_state=42):
    """
    Single-draw version. For the exhaustive/repeated version used for the
    final reported numbers, see pseudoreplication_check.py in this same
    folder -- a single arbitrary draw is not a reliable summary at small
    sample sizes.
    """
    deduped = deduplicate_by_composer(df, composer_col, random_state)
    results = {}
    for feature in feature_cols:
        _, naive_p = run_kruskal_wallis(df, feature, group_col)
        _, dedup_p = run_kruskal_wallis(deduped, feature, group_col)
        results[feature] = {'naive_p': round(naive_p, 4),
                             'deduplicated_p': round(dedup_p, 4)}
    return pd.DataFrame(results).T
