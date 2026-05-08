from flask import Blueprint, redirect, render_template, request, session, url_for

from config import CATEGORIES, CATEGORY_DETAILS
from routes.utils import current_user, login_required

main_bp = Blueprint("main", __name__)


@main_bp.app_context_processor
def inject_user():
    return {"current_user": current_user()}


@main_bp.route("/")
def home():
    return render_template("index.html")


@main_bp.route("/choose-path")
@login_required
def choose_path():
    return render_template("choose_path.html")


@main_bp.route("/choose-role")
@login_required
def old_choose_role():
    return redirect(url_for("main.choose_path"))


@main_bp.route("/find-mentor", methods=["GET", "POST"])
@login_required
def find_mentor():
    if request.method == "POST":
        mentee_name = request.form.get("mentee_name", "").strip()

        if not mentee_name:
            return render_template("find_mentor.html", error="Please enter your name.")

        session["mentee_name"] = mentee_name
        return redirect(url_for("main.categories"))

    return render_template("find_mentor.html")


@main_bp.route("/form", methods=["GET", "POST"])
@login_required
def old_form():
    return redirect(url_for("main.find_mentor"))


@main_bp.route("/categories")
@login_required
def categories():
    return render_template(
        "categories.html",
        categories=CATEGORIES,
        category_details=CATEGORY_DETAILS,
        mentee_name=session.get("mentee_name", "Student"),
    )


@main_bp.route("/department")
@login_required
def old_department():
    return redirect(url_for("main.categories"))


@main_bp.route("/mentors/<category>")
@login_required
def mentor_listing(category):
    if category not in CATEGORIES:
        return redirect(url_for("main.categories"))

    return render_template(
        "mentors.html",
        category=category,
        mentee_name=session.get("mentee_name", "Student"),
    )
