"""Rolling-window backtest entry points.

The implementation is intentionally small: portfolio rules are supplied as a
callable so the same engine can evaluate equal weight, minimum-risk,
maximum-Sharpe, and PCA portfolios.
"""

from collections.abc import Callable
import pandas as pd


def rolling_rebalance(returns: pd.DataFrame, lookback: int, rebalance: str,
                      weight_rule: Callable[[pd.DataFrame], pd.Series]) -> pd.DataFrame:
    """Return dated portfolio weights estimated from trailing observations."""
    weights = []
    for end in returns.resample(rebalance).last().index:
        history = returns.loc[:end].tail(lookback)
        if len(history) < lookback:
            continue
        w = weight_rule(history).rename(end)
        weights.append(w)
    return pd.DataFrame(weights)
