"""Leakage-aware cross-validation: walk-forward + purged K-fold with an embargo.

Overlapping labels leak information across the train/test boundary; purging drops the
`embargo` bars either side of each test fold from the training set (López de Prado).
"""
from __future__ import annotations

import numpy as np


def walk_forward(n: int, k: int = 5):
    """Expanding-window walk-forward: fold i trains on everything before it, tests on it."""
    for f in np.array_split(np.arange(n), k)[1:]:
        yield np.arange(f[0]), f


def purged_kfold(n: int, k: int = 5, embargo: int = 0):
    """Contiguous test folds; train excludes the fold plus `embargo` bars on each side."""
    idx = np.arange(n)
    for f in np.array_split(idx, k):
        if len(f) == 0:
            continue
        left, right = max(0, f[0] - embargo), min(n, f[-1] + 1 + embargo)
        yield np.concatenate([idx[:left], idx[right:]]), f
