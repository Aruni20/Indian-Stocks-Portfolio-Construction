# NSE portfolio replication

Source: supplied minute-bar archive, collapsed to each trading session's final close.

Training window: 1 Jul 2020 to 30 Jun 2025. Holdout: 1 Jul to 31 Dec 2025 (126 trading days).

Methods: long-only Monte-Carlo minimum variance, maximum Sharpe with a 1% annual risk-free rate, and PCA eigen portfolio. PCA selects the best Sharpe ratio among the first five components; absolute loadings are normalized to one.

## Six-month holdout returns

| Sector | Minimum variance | Maximum Sharpe | Eigen |
|---|---:|---:|---:|
| Auto | 19.14% | 9.18% | 14.93% |
| Banking | 2.30% | 7.74% | 10.57% |
| Consumer Durable | -13.32% | -7.14% | -12.14% |
| FMCG | -0.09% | 1.40% | -4.71% |
| Healthcare | -0.45% | 3.83% | 8.21% |
| IT | -5.10% | -10.50% | -3.89% |
| Metal | 8.32% | 5.53% | 6.84% |

The paper leaves its PCA loading transformation and risk-free return ambiguous. This implementation makes those decisions explicit. Omitted or unavailable constituents are recorded in `data_availability.json`.
