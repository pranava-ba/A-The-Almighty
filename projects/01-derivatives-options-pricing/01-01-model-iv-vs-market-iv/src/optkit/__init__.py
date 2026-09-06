"""optkit — the section-01 options toolkit: BSM + Greeks, lattices, IV inversion,
and the model-vs-market IV **surface** diff.

The pricing core (:mod:`~optkit.bsm`, :mod:`~optkit.lattice`, :mod:`~optkit.iv`) is
deliberately data-source-agnostic and reused across section 01's five subprojects; it
gets promoted into ``quant_lab/common/`` once the second subproject imports it (the same
"live in the subproject until a second consumer appears" rule the data lake followed).
The surface layer (:mod:`~optkit.chain`, :mod:`~optkit.surface`) is specific to
``01-01-model-iv-vs-market-iv``.
"""
from .bsm import bsm_price, delta, gamma, greeks, rho, theta, vega
from .chain import OptionChain, synthetic_smile_chain
from .iv import implied_vol, implied_vol_chain
from .lattice import crr_price, trinomial_price
from .surface import diff_surface, format_scorecard, model_surface, scorecard

__all__ = [
    # pricing core
    "bsm_price", "delta", "gamma", "vega", "theta", "rho", "greeks",
    "crr_price", "trinomial_price",
    "implied_vol", "implied_vol_chain",
    # surface layer (01-01)
    "OptionChain", "synthetic_smile_chain",
    "model_surface", "diff_surface", "scorecard", "format_scorecard",
]
