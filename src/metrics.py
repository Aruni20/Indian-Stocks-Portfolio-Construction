"""Common portfolio performance metrics."""

import numpy as np
import pandas as pd

def performance_metrics(returns: pd.Series, periods_per_year: int = 252) -> dict:
    returns = returns.dropna(); wealth = (1 + returns).cumprod()
    dd = wealth / wealth.cummax() - 1; years = len(returns) / periods_per_year
    cagr = wealth.iloc[-1] ** (1 / years) - 1 if years else np.nan
    return {"cumulative_return": wealth.iloc[-1]-1, "cagr": cagr, "volatility": returns.std()*np.sqrt(periods_per_year), "maximum_drawdown": dd.min()}
