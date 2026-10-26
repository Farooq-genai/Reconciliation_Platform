
from typing import Any
import pandas as pd


EXPECTED_FIELDS = ["name", "age", "city"]


def validate_dataframe(df: pd.DataFrame) -> list[dict[str, Any]]:
    actual_fields = list(df.columns)

    missing_fields = set(EXPECTED_FIELDS) - set(actual_fields)
    extra_fields = set(actual_fields) - set(EXPECTED_FIELDS)

    if missing_fields or extra_fields:
        raise ValueError(
            f"Header mismatch. Missing fields: {sorted(missing_fields)}; "
            f"Extra fields: {sorted(extra_fields)}"
        )

    records = df[EXPECTED_FIELDS].to_dict(orient="records")

    for row_number, record in enumerate(records, start=2):
        if not isinstance(record["name"], str) or not record["name"].strip():
            raise ValueError(f"Invalid name at row {row_number}")

        age = record["age"]

        if isinstance(age, bool) or not isinstance(age, (int, float)):
            raise ValueError(f"Age must be numeric at row {row_number}")

        if not float(age).is_integer() or not 0 <= age <= 120:
            raise ValueError(f"Age must be an integer between 0 and 120 at row {row_number}")

        if not isinstance(record["city"], str) or not record["city"].strip():
            raise ValueError(f"Invalid city at row {row_number}")

        record["age"] = int(age)
        record["name"] = record["name"].strip()
        record["city"] = record["city"].strip()

    return records
