from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from flask import current_app, request


def utc_now():
    return datetime.now(timezone.utc)


def allowed_file(filename):
    if not filename or "." not in filename:
        return False

    extension = Path(filename).suffix.lower().lstrip(".")

    return extension in current_app.config["ALLOWED_EXTENSIONS"]


def generate_unique_filename(extension):
    extension = str(extension or "").lstrip(".").lower()

    if not extension:
        return uuid4().hex

    return f"{uuid4().hex}.{extension}"


def get_client_ip():
    forwarded_for = request.headers.get(
        "X-Forwarded-For",
        ""
    )

    if forwarded_for:
        return forwarded_for.split(",")[0].strip()

    return request.remote_addr


def get_user_agent():
    return request.headers.get(
        "User-Agent",
        ""
    )[:1000]


def ensure_directory(path):
    directory = Path(path)
    directory.mkdir(
        parents=True,
        exist_ok=True
    )
    return directory


def storage_path(folder, *parts):
    base_path = Path(
        current_app.config[folder]
    )

    path = base_path.joinpath(*parts)
    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    return path


def human_file_size(size):
    size = float(size)

    for unit in (
        "B",
        "KB",
        "MB",
        "GB",
        "TB"
    ):
        if size < 1024:
            return f"{size:.1f} {unit}"

        size /= 1024

    return f"{size:.1f} PB"


def truncate_text(value, length=100):
    value = str(value or "").strip()

    if len(value) <= length:
        return value

    return f"{value[:length - 3]}..."


def normalize_email(email):
    return str(
        email or ""
    ).strip().lower()


def normalize_text(value):
    return " ".join(
        str(value or "").strip().split()
    )