import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-this")

    database_url = os.environ.get("DATABASE_URL")
    if database_url and database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)

    SQLALCHEMY_DATABASE_URI = database_url or f"sqlite:///{BASE_DIR / 'mentorconnect.db'}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")

    UPLOAD_FOLDER = BASE_DIR / "static" / "uploads"
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024
    ALLOWED_IMAGE_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}


BRANCHES = ["MECH", "COMPS", "IT", "EXTC"]
YEARS = ["SE", "TE", "BE"]
CATEGORIES = ["Studies", "Projects", "Cultural", "Sports", "Placements"]

CATEGORY_DETAILS = {
    "Studies": {
        "icon": "bi-journal-code",
        "description": "Subject support, notes, exams, and academic guidance.",
    },
    "Projects": {
        "icon": "bi-kanban",
        "description": "Mini projects, final year work, reports, and demos.",
    },
    "Cultural": {
        "icon": "bi-music-note-beamed",
        "description": "Dance, music, drama, anchoring, debate, and events.",
    },
    "Sports": {
        "icon": "bi-trophy",
        "description": "Training, team selection, fitness, and tournaments.",
    },
    "Placements": {
        "icon": "bi-briefcase",
        "description": "Resume, aptitude, interviews, and career guidance.",
    },
}
