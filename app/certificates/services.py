import secrets
from pathlib import Path

import pandas as pd
from flask import current_app
from werkzeug.utils import secure_filename

from .validators import is_allowed_file, validate_upload_file

NAME_COLUMNS = {
    "name",
    "student_name",
    "student name",
    "recipient_name",
    "recipient name"
}

COLLEGE_COLUMNS = {
    "college_name",
    "college name",
    "college",
    "institution",
    "institution_name"
}


def normalize_column_name(value):
    return str(value).strip().lower().replace("-", "_").replace(" ", "_")


def find_column(columns, allowed_columns):
    normalized = {
        normalize_column_name(column): column
        for column in columns
    }

    for allowed in allowed_columns:
        key = normalize_column_name(allowed)

        if key in normalized:
            return normalized[key]

    return None


def _standardize_dataframe(dataframe):
    if dataframe.empty:
        raise ValueError(
            "The uploaded file contains no records."
        )

    name_column = find_column(
        dataframe.columns,
        NAME_COLUMNS
    )

    college_column = find_column(
        dataframe.columns,
        COLLEGE_COLUMNS
    )

    if not name_column:
        raise ValueError(
            "A name column was not found."
        )

    if not college_column:
        raise ValueError(
            "A college_name column was not found."
        )

    dataframe = dataframe[
        [name_column, college_column]
    ].copy()

    dataframe.columns = [
        "name",
        "college_name"
    ]

    dataframe["name"] = (
        dataframe["name"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    dataframe["college_name"] = (
        dataframe["college_name"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    dataframe = dataframe[
        (dataframe["name"] != "") &
        (dataframe["college_name"] != "")
    ].reset_index(drop=True)

    if dataframe.empty:
        raise ValueError(
            "No valid name and college_name records were found."
        )

    return dataframe


def _read_dataframe_by_extension(file_or_path, extension):
    try:
        if extension == ".csv":
            dataframe = pd.read_csv(file_or_path)
        elif extension in {".xlsx", ".xls"}:
            dataframe = pd.read_excel(file_or_path)
        else:
            raise ValueError("Unsupported file format.")
    except ValueError:
        raise
    except Exception as exc:
        raise ValueError(
            "Unable to read the uploaded file."
        ) from exc

    return dataframe


def read_certificate_file(file):
    """Read + validate an in-memory upload (used for the initial preview)."""
    valid, error = validate_upload_file(
        file,
        current_app.config["ALLOWED_EXTENSIONS"]
    )

    if not valid:
        raise ValueError(error)

    extension = Path(file.filename).suffix.lower()

    file.seek(0)
    dataframe = _read_dataframe_by_extension(file, extension)

    return _standardize_dataframe(dataframe)


def read_certificate_file_from_path(path, original_filename):
    """Read + validate a file already persisted on disk (used when actually
    generating certificates, since the browser cannot re-submit a <input
    type=file> across a redirect/preview step)."""
    if not is_allowed_file(
        original_filename,
        current_app.config["ALLOWED_EXTENSIONS"]
    ):
        raise ValueError("Only Excel and CSV files are allowed.")

    extension = Path(original_filename).suffix.lower()

    dataframe = _read_dataframe_by_extension(str(path), extension)

    return _standardize_dataframe(dataframe)


def get_upload_path(filename):
    upload_folder = Path(
        current_app.config["UPLOAD_FOLDER"]
    )

    upload_folder.mkdir(
        parents=True,
        exist_ok=True
    )

    safe_name = secure_filename(
        Path(filename).name
    )

    if not safe_name:
        raise ValueError(
            "Invalid uploaded filename."
        )

    return upload_folder / f"{secrets.token_hex(8)}_{safe_name}"


def save_temp_upload(file):
    """Persist an in-memory upload to the temp folder so it can be picked
    back up by the generation step after the preview page is shown."""
    temp_folder = Path(
        current_app.config["TEMP_FOLDER"]
    )

    temp_folder.mkdir(
        parents=True,
        exist_ok=True
    )

    extension = Path(file.filename).suffix.lower()
    temp_name = f"{secrets.token_hex(16)}{extension}"

    file.seek(0)
    file.save(temp_folder / temp_name)
    file.seek(0)

    return temp_name


def get_temp_path(temp_name):
    temp_folder = Path(
        current_app.config["TEMP_FOLDER"]
    ).resolve()

    safe_name = secure_filename(temp_name)

    if not safe_name:
        raise ValueError("Invalid upload reference.")

    temp_path = (temp_folder / safe_name).resolve()

    if temp_folder != temp_path and temp_folder not in temp_path.parents:
        raise ValueError("Invalid upload reference.")

    return temp_path
