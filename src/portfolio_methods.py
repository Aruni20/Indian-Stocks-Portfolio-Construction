"""Long-only portfolio construction utilities."""
import numpy as np

def normalize_long_only(weights, max_weight=1.0):
    w=np.nan_to_num(np.asarray(weights,dtype=float),nan=0.0)
    w=np.maximum(w,0.0)
    if max_weight < 1.0:
        w=np.minimum(w,max_weight)
    total=w.sum()
    return w/total if total > 0 else np.ones_like(w)/len(w)

def equal_weight(n, max_weight=1.0):
    return normalize_long_only(np.ones(n), max_weight)

def portfolio_stats(weights, mean_returns, covariance, risk_free=0.01):
    annual_return=float(weights @ mean_returns)
    annual_risk=float(np.sqrt(weights @ covariance @ weights))
    sharpe=(annual_return-risk_free)/annual_risk if annual_risk else np.nan
    return annual_return, annual_risk, sharpe
