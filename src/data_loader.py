"""Data-loading helpers for Indian equity price data."""

from pathlib import Path
import pandas as pd


def load_prices(path: str | Path) -> pd.DataFrame:
    """Load a CSV containing a date column and one or more price columns."""
    frame = pd.read_csv(path)
    date_col = next((c for c in frame.columns if c.lower() in {"date", "datetime", "timestamp"}), None)
    if date_col is None:
        raise ValueError("Input data must contain Date, Datetime, or Timestamp")
    frame[date_col] = pd.to_datetime(frame[date_col])
    return frame.sort_values(date_col).set_index(date_col)
