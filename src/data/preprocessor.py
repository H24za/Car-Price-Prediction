import numpy as np
import pandas as pd


def replace_categorical_by_numerical(data: pd.DataFrame) -> pd.DataFrame:
    data = data.copy()
    data.loc[:, 'Levy'] = data['Levy'].replace({'-': 0})
    data.loc[:, 'Levy'] = pd.to_numeric(data['Levy'], errors='coerce').fillna(0)

    # remove textual tokens and coerce
    data.loc[:, 'Engine volume'] = data['Engine volume'].astype(str).str.replace('Turbo', '', regex=False)
    data.loc[:, 'Engine volume'] = pd.to_numeric(data['Engine volume'], errors='coerce')

    data.loc[:, 'Mileage'] = data['Mileage'].astype(str).str.replace('km', '', regex=False)
    data.loc[:, 'Mileage'] = pd.to_numeric(data['Mileage'], errors='coerce')

    return data


def column_transformations(data: pd.DataFrame) -> pd.DataFrame:
    # Use log1p to avoid -inf for zeros
    data['Mileage_log'] = np.log1p(data['Mileage']).replace(-np.inf, 1e-6)
    data['Levy_log'] = np.log1p(data['Levy']).replace(-np.inf, 1e-6)
    data['Engine_volume_log'] = np.log1p(data['Engine volume']).replace(-np.inf, 1e-6)

    return data


def clean_outliers(df: pd.DataFrame, cols) -> pd.DataFrame:
    df = df.copy()
    for col in cols:
        if col not in df.columns:
            continue
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1

        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr

        df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]

    return df


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    current_year = pd.Timestamp.now().year
    # Prod. year might be non-numeric; coerce safely first
    if 'Prod. year' in df.columns:
        df['Prod. year'] = pd.to_numeric(df['Prod. year'], errors='coerce')
    df['Age'] = current_year - df['Prod. year']

    # Add more features here if needed

    return df


def preprocessing_pipeline(df: pd.DataFrame) -> pd.DataFrame:
    """A small, defensive preprocessing pipeline used by the notebooks.

    Steps:
    - drop duplicates
    - coerce categorical numeric fields (Levy, Engine volume, Mileage)
    - remove outliers on key numeric columns
    - engineer simple features (Age)
    - drop a small set of unused columns
    """
    print("Preprocessing started...")
    print(f"Initial shape: {df.shape}")

    df = df.drop_duplicates()
    print(f"After dropping duplicates: {df.shape}")

    print("Replacing categorical values...")
    df = replace_categorical_by_numerical(df)

    df = clean_outliers(df, ['Price', 'Levy', 'Engine volume', 'Mileage'])
    print(f"After cleaning outliers: {df.shape}")

    # optional transformations
    # df = column_transformations(df)

    print("Feature engineering...")
    df = engineer_features(df)

    print("Dropping columns...")
    drop_cols = [c for c in ['ID', 'Doors', 'Prod. year'] if c in df.columns]
    if drop_cols:
        df = df.drop(drop_cols, axis=1)

    print("Final shape:", df.shape)

    return df
