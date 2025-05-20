import pandas as pd
import numpy as np
from pathlib import Path
from scipy.stats import zscore


def load_solar_data(data_type='clean'):
    """Load solar data from specified directory"""
    data_dir = Path(__file__).parent.parent / "data"
    file_map = {
        'clean': {
            'Benin': 'clean/benin_clean.csv',
            'Togo': 'clean/togo_clean.csv',
            'Sierra Leone': 'clean/sierraleone_clean.csv'
        },
        'raw': {
            'Sierra Leone': 'sierraleone-bumbuna.csv',
            'Togo': 'togo-dapaong_qc.csv',
            'Benin': 'benin-malanville.csv'
        }
    }

    dfs = []
    for country, rel_path in file_map[data_type].items():
        try:
            df = pd.read_csv(
                data_dir / rel_path,
                parse_dates=['Timestamp'] if data_type == 'raw' else None
            )
            df['Country'] = country
            dfs.append(df)
        except FileNotFoundError:
            continue

    return pd.concat(dfs) if dfs else pd.DataFrame()


def analyze_missing_data(df):
    """Generate missing data analysis"""
    if df.empty:
        return None

    missing = df.isna().sum()
    threshold = 0.05 * len(df)
    return {
        'missing_counts': missing,
        'significant_missing': missing[missing > threshold],
        'threshold': threshold
    }


def detect_outliers(df, columns):
    """Identify outliers using z-score"""
    outliers = {}
    for col in columns:
        if col in df.columns:
            col_data = df[col].dropna()
            if len(col_data) > 0:
                z_scores = np.abs(zscore(col_data))
                outliers[col] = df[z_scores > 3]
    return outliers


def prepare_comparison_data(df, countries, metric):
    """Prepare data for country comparison"""
    if df.empty:
        return None

    filtered = df[df['Country'].isin(countries)] if countries else df
    stats = filtered.groupby('Country')[metric].describe()
    samples = [filtered[filtered['Country'] == c][metric] for c in stats.index]

    return {
        'stats': stats,
        'samples': samples,
        'filtered_data': filtered
    }