from pathlib import Path


def is_allowed_file(filename, allowed_extensions):
    if not filename or "." not in filename:
        return False

    extension = Path(filename).suffix.lower().lstrip(".")

    return extension in allowed_extensions


def validate_upload_file(file, allowed_extensions):
    if not file or not file.filename:
        return False, "Please select an Excel or CSV file."

    if not is_allowed_file(
        file.filename,
        allowed_extensions
    ):
        return False, "Only Excel and CSV files are allowed."

    return True, None