# This can be improved further based on specific requirements and data types.
import pandas as pd
import numpy as np


def clean_dataframe(df: pd.DataFrame) -> dict:
    report = {
        "dropped_columns": 0,
        "missing_values_fixed": 0,
        "type_conversions": 0
    }

    # 1. Drop fully empty columns
    before_cols = df.shape[1]
    df = df.dropna(axis=1, how="all")
    report["dropped_columns"] = before_cols - df.shape[1]

    # 2. Standardize column names
    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace(r"[^a-z0-9_]", "", regex=True)
    )

    # 3. Strip whitespace from string columns
    for col in df.select_dtypes(include=["object"]).columns:
        df[col] = df[col].astype(str).str.strip()

    # 4. Type conversion attempts
    for col in df.columns:
        original_dtype = df[col].dtype

        # Try numeric conversion
        numeric_series = pd.to_numeric(df[col], errors="coerce")
        if numeric_series.notna().sum() > 0 and numeric_series.notna().sum() >= df[col].notna().sum() * 0.8:
            df[col] = numeric_series
            if original_dtype != df[col].dtype:
                report["type_conversions"] += 1
            continue

        # Try datetime conversion
        datetime_series = pd.to_datetime(df[col], errors="coerce", infer_datetime_format=True)
        if datetime_series.notna().sum() > 0 and datetime_series.notna().sum() >= df[col].notna().sum() * 0.8:
            df[col] = datetime_series
            if original_dtype != df[col].dtype:
                report["type_conversions"] += 1

    # 5. Missing value handling
    for col in df.columns:
        missing_before = df[col].isna().sum()
        if missing_before == 0:
            continue

        if pd.api.types.is_numeric_dtype(df[col]):
            median = df[col].median()
            df[col] = df[col].fillna(median)
        else:
            mode = df[col].mode(dropna=True)
            if not mode.empty:
                df[col] = df[col].fillna(mode[0])

        missing_after = df[col].isna().sum()
        report["missing_values_fixed"] += (missing_before - missing_after)

    return {
        "dataframe": df,
        "report": report
    }
