from flask import Blueprint, abort, flash, jsonify, redirect, render_template, request, url_for

from config import BRANCHES, CATEGORIES, YEARS
from models import Mentor, db
from routes.utils import current_user, login_required, save_uploaded_photo

mentors_bp = Blueprint("mentors", __name__)


@mentors_bp.route("/become-mentor", methods=["GET", "POST"])
@login_required
def become_mentor():
    user = current_user()
    existing_profile = Mentor.query.filter_by(user_id=user.id).first()

    if request.method == "POST":
        if existing_profile:
            flash("You already have a mentor profile. Edit it from My Profile.", "warning")
            return redirect(url_for("mentors.my_profile"))

        mentor = build_mentor_from_form(user)

        if isinstance(mentor, str):
            return render_template(
                "mentor_form.html",
                branches=BRANCHES,
                years=YEARS,
                categories=CATEGORIES,
                error=mentor,
                mentor=None,
            )

        db.session.add(mentor)
        db.session.commit()

        flash("Your mentor profile has been created.", "success")
        return redirect(url_for("mentors.my_profile"))

    return render_template(
        "mentor_form.html",
        branches=BRANCHES,
        years=YEARS,
        categories=CATEGORIES,
        mentor=None,
    )


@mentors_bp.route("/mentor-register", methods=["GET", "POST"])
@login_required
def old_mentor_register():
    return redirect(url_for("mentors.become_mentor"))


@mentors_bp.route("/my-profile")
@login_required
def my_profile():
    mentor = Mentor.query.filter_by(user_id=current_user().id).first()
    return render_template("profile.html", mentor=mentor)


@mentors_bp.route("/edit-profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    mentor = Mentor.query.filter_by(user_id=current_user().id).first()

    if not mentor:
        flash("Create a mentor profile first.", "warning")
        return redirect(url_for("mentors.become_mentor"))

    if request.method == "POST":
        error = update_mentor_from_form(mentor)

        if error:
            return render_template(
                "mentor_form.html",
                branches=BRANCHES,
                years=YEARS,
                categories=CATEGORIES,
                error=error,
                mentor=mentor,
            )

        db.session.commit()
        flash("Your mentor profile has been updated.", "success")
        return redirect(url_for("mentors.my_profile"))

    return render_template(
        "mentor_form.html",
        branches=BRANCHES,
        years=YEARS,
        categories=CATEGORIES,
        mentor=mentor,
    )


@mentors_bp.route("/delete-profile", methods=["POST"])
@login_required
def delete_profile():
    mentor = Mentor.query.filter_by(user_id=current_user().id).first()

    if not mentor:
        abort(404)

    db.session.delete(mentor)
    db.session.commit()

    flash("Your mentor profile has been deleted.", "info")
    return redirect(url_for("main.choose_path"))


@mentors_bp.route("/api/mentors")
@login_required
def api_mentors():
    category = request.args.get("category", "")
    search = request.args.get("search", "").strip().lower()

    query = Mentor.query

    if category in CATEGORIES:
        query = query.filter_by(category=category)

    if search:
        query = query.filter(Mentor.expertise.ilike(f"%{search}%"))

    mentors = query.order_by(Mentor.created_at.desc()).all()
    return jsonify([mentor.to_dict() for mentor in mentors])


@mentors_bp.route("/search")
@login_required
def search():
    return api_mentors()


def build_mentor_from_form(user):
    mentor = Mentor(user_id=user.id)
    error = update_mentor_from_form(mentor)

    if error:
        return error

    return mentor


def update_mentor_from_form(mentor):
    mentor_name = request.form.get("mentor_name", "").strip()
    branch = request.form.get("branch", "").strip()
    year = request.form.get("year", "").strip()
    expertise = request.form.get("expertise", "").strip()
    category = request.form.get("category", "").strip()
    email = request.form.get("email", "").strip()
    linkedin = request.form.get("linkedin", "").strip()

    if linkedin and not linkedin.startswith(("http://", "https://")):
        linkedin = f"https://linkedin.com/in/{linkedin.lstrip('@')}"

    if not mentor_name or not expertise or not email:
        return "Please fill all required fields."

    if branch not in BRANCHES:
        return "Please select a valid branch."

    if year not in YEARS:
        return "Please select a valid year."

    if category not in CATEGORIES:
        return "Please select a valid category."

    try:
        photo_path = save_uploaded_photo(request.files.get("photo"), mentor.photo_path)
    except ValueError as error:
        return str(error)

    mentor.mentor_name = mentor_name
    mentor.branch = branch
    mentor.year = year
    mentor.expertise = expertise
    mentor.category = category
    mentor.email = email
    mentor.linkedin = linkedin
    mentor.photo_path = photo_path

    return None
