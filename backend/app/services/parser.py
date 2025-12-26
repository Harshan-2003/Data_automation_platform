import os
import pandas as pd

MAX_FILE_SIZE_MB = 50          # hard safety limit
MAX_ROWS = 100_000             # row cap
ENCODINGS = ["utf-8", "latin-1"]

class FileParsingError(Exception):
    pass


def _check_file_size(file_path: str):
    size_mb = os.path.getsize(file_path) / (1024 * 1024)
    if size_mb > MAX_FILE_SIZE_MB:
        raise FileParsingError(f"File too large: {size_mb:.2f} MB")


def _read_with_encodings(reader_func, file_path: str, **kwargs):
    last_error = None
    for enc in ENCODINGS:
        try:
            return reader_func(file_path, encoding=enc, **kwargs)
        except Exception as e:
            last_error = e
    raise FileParsingError(f"Encoding failed: {last_error}")


def parse_file(file_path: str) -> dict:
    _check_file_size(file_path)

    ext = os.path.splitext(file_path)[1].lower()

    try:
        if ext == ".csv":
            df = _read_with_encodings(
                pd.read_csv,
                file_path,
                nrows=MAX_ROWS
            )

        elif ext == ".xlsx":
            df = pd.read_excel(
                file_path,
                nrows=MAX_ROWS,
                engine="openpyxl"
            )

        elif ext == ".json":
            df = _read_with_encodings(
                pd.read_json,
                file_path
            )
            df = df.head(MAX_ROWS)

        else:
            raise FileParsingError("Unsupported file format")

    except Exception as e:
        raise FileParsingError(str(e))

    return {
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "column_names": list(df.columns),
        "dataframe": df
    }
