from __future__ import annotations

from pathlib import Path
from uuid import uuid4

from flask import current_app
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}
UPLOAD_FOLDER = "uploads"


def allowed_file(filename: str) -> bool:
    if not filename or "." not in filename:
        return False
    suffix = Path(filename).suffix.lower().lstrip(".")
    return suffix in ALLOWED_EXTENSIONS


def save_image(file: FileStorage | None) -> str | None:
    if file is None or not file.filename:
        return None

    if not allowed_file(file.filename):
        return None

    filename = f"{uuid4().hex}_{secure_filename(file.filename)}"
    folder = Path(current_app.root_path) / "static" / UPLOAD_FOLDER
    folder.mkdir(parents=True, exist_ok=True)
    file.save(folder / filename)
    return f"{UPLOAD_FOLDER}/{filename}"
