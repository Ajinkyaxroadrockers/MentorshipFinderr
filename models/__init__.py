from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    google_id = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    profile_pic = db.Column(db.String(500))

    mentor_profile = db.relationship(
        "Mentor",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )


class Mentor(db.Model):
    __tablename__ = "mentors"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    mentor_name = db.Column(db.String(120), nullable=False)
    branch = db.Column(db.String(20), nullable=False)
    year = db.Column(db.String(10), nullable=False)
    expertise = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    photo_path = db.Column(db.String(500), nullable=False)
    linkedin = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    user = db.relationship("User", back_populates="mentor_profile")

    def to_dict(self):
        return {
            "id": self.id,
            "mentor_name": self.mentor_name,
            "branch": self.branch,
            "year": self.year,
            "expertise": self.expertise,
            "category": self.category,
            "email": self.email,
            "photo_path": self.photo_path,
            "linkedin": self.linkedin or "",
        }
