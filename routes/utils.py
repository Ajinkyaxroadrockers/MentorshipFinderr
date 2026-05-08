from functools import wraps
from pathlib import Path
from uuid import uuid4

from flask import current_app, flash, redirect, session, url_for
from werkzeug.utils import secure_filename

from models import User


def current_user():
    user_id = session.get("user_id")
    if not user_id:
        return None
    return User.query.get(user_id)


def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if not current_user():
            flash("Please sign in with Google first.", "warning")
            return redirect(url_for("auth.login"))
        return view(*args, **kwargs)

    return wrapped_view


def allowed_image(filename):
    extension = filename.rsplit(".", 1)[-1].lower()
    return "." in filename and extension in current_app.config["ALLOWED_IMAGE_EXTENSIONS"]


def save_uploaded_photo(file_storage, old_photo_path=None):
    if not file_storage or file_storage.filename == "":
        return old_photo_path or url_for("static", filename="uploads/default-avatar.svg")

    if not allowed_image(file_storage.filename):
        raise ValueError("Only PNG, JPG, JPEG, and WEBP images are allowed.")

    upload_folder = Path(current_app.config["UPLOAD_FOLDER"])
    upload_folder.mkdir(parents=True, exist_ok=True)

    filename = secure_filename(file_storage.filename)
    unique_filename = f"{uuid4().hex}_{filename}"
    file_storage.save(upload_folder / unique_filename)

    return url_for("static", filename=f"uploads/{unique_filename}")
