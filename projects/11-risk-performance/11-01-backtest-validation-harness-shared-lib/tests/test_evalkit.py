"""Offline tests for the shared eval backbone."""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from evalkit import (  # noqa: E402
    deflated_sharpe, max_drawdown, probabilistic_sharpe, purged_kfold, sharpe,
    tearsheet, turnover, walk_forward,
)

rng = np.random.default_rng(0)


def test_sharpe_sign_and_degenerate():
    up = rng.normal(0.001, 0.01, 500)
    assert sharpe(up) > 0
    assert np.isnan(sharpe([0.01, 0.01, 0.01]))     # zero variance
    assert np.isnan(sharpe([0.01]))                 # too short


def test_max_drawdown():
    assert max_drawdown([0.1, 0.1, 0.1]) == 0.0     # monotonic up
    assert max_drawdown([0.1, -0.5, 0.1]) < 0       # a dip


def test_psr_monotonic_in_mean():
    lo = rng.normal(0.0005, 0.01, 400)
    hi = lo + 0.001
    assert probabilistic_sharpe(hi) > probabilistic_sharpe(lo)


def test_deflated_le_psr_and_drops_with_trials():
    r = rng.normal(0.001, 0.01, 400)
    base = probabilistic_sharpe(r, 0.0)
    dsr = deflated_sharpe(r, sr_trials_std=0.05, n_trials=100)
    assert dsr <= base + 1e-9                        # selection-bias discount never raises it
    assert deflated_sharpe(r, 0.05, 1000) <= deflated_sharpe(r, 0.05, 10)


def test_turnover():
    assert turnover([[0.5, 0.5], [0.5, 0.5]]) == 0.0
    assert turnover([[1.0, 0.0], [0.0, 1.0]]) == 2.0


def test_tearsheet_keys():
    t = tearsheet(rng.normal(0.001, 0.01, 300), n_trials=50, sr_trials_std=0.05)
    assert {"n", "ann_return", "sharpe", "max_drawdown", "psr", "hit_rate",
            "deflated_sharpe"} <= set(t)


def test_purged_kfold_and_walkforward():
    folds = list(purged_kfold(100, k=5, embargo=2))
    assert len(folds) == 5
    test_union = np.concatenate([te for _, te in folds])
    assert sorted(test_union.tolist()) == list(range(100))     # test folds partition
    for tr, te in folds:                                       # embargo purged from train
        assert not (set(range(te[0] - 2, te[-1] + 3)) & set(tr.tolist()) - set(te.tolist()))
    assert len(list(walk_forward(100, k=5))) == 4              # expanding: first fold is train-only
