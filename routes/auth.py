from authlib.integrations.flask_client import OAuth
from flask import Blueprint, current_app, flash, redirect, session, url_for

from models import User, db

auth_bp = Blueprint("auth", __name__)
oauth = OAuth()


@auth_bp.record_once
def register_google_oauth(state):
    app = state.app
    oauth.register(
        name="google",
        client_id=app.config["GOOGLE_CLIENT_ID"],
        client_secret=app.config["GOOGLE_CLIENT_SECRET"],
        server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
        client_kwargs={"scope": "openid email profile"},
    )


@auth_bp.route("/login")
def login():
    if not current_app.config["GOOGLE_CLIENT_ID"]:
        flash("Google OAuth is not configured yet.", "danger")
        return redirect(url_for("main.home"))

    redirect_uri = url_for("auth.callback", _external=True)
    return oauth.google.authorize_redirect(redirect_uri)


@auth_bp.route("/auth/callback")
def callback():
    token = oauth.google.authorize_access_token()
    user_info = token.get("userinfo") or oauth.google.userinfo()

    google_id = user_info["sub"]
    email = user_info["email"]
    name = user_info.get("name", email.split("@")[0])
    profile_pic = user_info.get("picture", "")

    user = User.query.filter_by(google_id=google_id).first()

    if not user:
        user = User(google_id=google_id, email=email, name=name, profile_pic=profile_pic)
        db.session.add(user)
    else:
        user.name = name
        user.email = email
        user.profile_pic = profile_pic

    db.session.commit()
    session["user_id"] = user.id

    flash(f"Welcome, {user.name}!", "success")
    return redirect(url_for("main.find_mentor"))


@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("main.home"))
