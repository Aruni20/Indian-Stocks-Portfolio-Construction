"""Performance metrics used by the report."""

import numpy as np
import pandas as pd


def performance_metrics(returns: pd.Series, periods_per_year: int = 252) -> dict[str, float]:
    returns = returns.dropna()
    wealth = (1 + returns).cumprod()
    years = len(returns) / periods_per_year
    cagr = wealth.iloc[-1] ** (1 / years) - 1 if years else np.nan
    drawdown = wealth / wealth.cummax() - 1
    downside = returns[returns < 0].std() * np.sqrt(periods_per_year)
    vol = returns.std() * np.sqrt(periods_per_year)
    return {
        "cumulative_return": wealth.iloc[-1] - 1,
        "cagr": cagr,
        "volatility": vol,
        "sharpe": returns.mean() / returns.std() * np.sqrt(periods_per_year) if returns.std() else np.nan,
        "sortino": returns.mean() * periods_per_year / downside if downside else np.nan,
        "maximum_drawdown": drawdown.min(),
        "calmar": cagr / abs(drawdown.min()) if drawdown.min() else np.nan,
    }
