from pathlib import Path

from flask import current_app
from werkzeug.utils import secure_filename


def get_storage_folder(folder_name):
    folder = Path(
        current_app.config[folder_name]
    )
    folder.mkdir(
        parents=True,
        exist_ok=True
    )
    return folder


def get_upload_folder():
    return get_storage_folder(
        "UPLOAD_FOLDER"
    )


def get_generated_folder():
    return get_storage_folder(
        "GENERATED_FOLDER"
    )


def get_temp_folder():
    return get_storage_folder(
        "TEMP_FOLDER"
    )


def create_user_storage(user_id):
    folder = (
        get_generated_folder() /
        str(user_id)
    )

    folder.mkdir(
        parents=True,
        exist_ok=True
    )

    return folder


def create_batch_storage(
    user_id,
    batch_id
):
    folder = (
        create_user_storage(user_id) /
        str(batch_id)
    )

    folder.mkdir(
        parents=True,
        exist_ok=True
    )

    return folder


def safe_filename(
    filename,
    fallback="file"
):
    filename = secure_filename(
        Path(str(filename or "")).name
    )

    return filename or fallback


def resolve_generated_file(relative_path):
    base_folder = get_generated_folder().resolve()

    file_path = (
        base_folder /
        str(relative_path)
    ).resolve()

    if (
        file_path != base_folder
        and base_folder not in file_path.parents
    ):
        raise ValueError(
            "Invalid storage path."
        )

    return file_path


def delete_file(path):
    file_path = Path(path)

    if not file_path.is_file():
        return False

    file_path.unlink()

    return True