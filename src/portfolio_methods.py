from __future__ import annotations

import numpy as np


def normalize_long_only(weights: np.ndarray, max_weight: float = 1.0) -> np.ndarray:
    """Clip negative/oversized weights and normalize them to sum to one."""
    w = np.nan_to_num(np.asarray(weights, dtype=float), nan=0.0)
    w = np.maximum(w, 0.0)
    if max_weight < 1.0:
        w = np.minimum(w, max_weight)
    total = w.sum()
    return w / total if total > 0 else np.ones_like(w) / len(w)


def equal_weight(n: int, max_weight: float = 1.0) -> np.ndarray:
    return normalize_long_only(np.ones(n), max_weight)


def _returns_frame(returns):
    import pandas as pd
    return returns if isinstance(returns, pd.DataFrame) else pd.DataFrame(returns)


def minimum_variance(returns, max_weight: float = 1.0) -> np.ndarray:
    """Long-only inverse-variance proxy for the minimum-risk portfolio."""
    frame = _returns_frame(returns)
    variance = frame.var().to_numpy(dtype=float)
    return normalize_long_only(1.0 / np.maximum(variance, 1e-12), max_weight)


def max_sharpe(returns, risk_free: float = 0.01, max_weight: float = 1.0) -> np.ndarray:
    """Long-only positive excess-return allocation, normalized to invest 100%."""
    frame = _returns_frame(returns)
    excess = frame.mean().to_numpy(dtype=float) * 252.0 - risk_free
    return normalize_long_only(np.maximum(excess, 0.0), max_weight)


def eigenportfolio(returns, component: int = 0, max_weight: float = 1.0) -> np.ndarray:
    """Long-only normalized absolute loading of a PCA covariance eigenvector."""
    frame = _returns_frame(returns).dropna()
    cov = np.cov(frame.to_numpy(), rowvar=False)
    values, vectors = np.linalg.eigh(cov)
    loading = vectors[:, np.argsort(values)[::-1][component]]
    return normalize_long_only(np.abs(loading), max_weight)


def portfolio_stats(weights, mean_returns, covariance, risk_free=0.01):
    annual_return = float(weights @ mean_returns)
    annual_risk = float(np.sqrt(weights @ covariance @ weights))
    sharpe = (annual_return - risk_free) / annual_risk if annual_risk else np.nan
    return annual_return, annual_risk, sharpe
