import io
import pandas as pd


def read_uploaded_file(filename: str, content: bytes) -> pd.DataFrame:
    extension = filename.rsplit(".", 1)[-1].lower()

    if extension == "csv":
        df = pd.read_csv(io.BytesIO(content))
    elif extension == "xlsx":
        df = pd.read_excel(io.BytesIO(content), engine="openpyxl")
    else:
        raise ValueError("Only CSV and XLSX files are supported")

    if df.empty:
        raise ValueError("The uploaded file contains no data rows")

    if df.columns.empty:
        raise ValueError("The uploaded file has no headers")

    if df.columns.duplicated().any():
        raise ValueError("Duplicate column headers are not allowed")

    if df.columns.isna().any():
        raise ValueError("Column headers cannot be empty")

    df.columns = df.columns.astype(str).str.strip()

    if any(not column for column in df.columns):
        raise ValueError("Column headers cannot be empty")

    if df.columns.duplicated().any():
        raise ValueError("Duplicate column headers are not allowed")

    if df.isna().any().any():
        raise ValueError("Missing values are not allowed")

    return df
