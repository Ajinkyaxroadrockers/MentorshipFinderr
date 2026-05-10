from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix
import cloudinary

from config import Config
from models import db
from routes.auth import auth_bp, oauth
from routes.main import main_bp
from routes.mentors import mentors_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)

    cloudinary.config(
        cloud_name=app.config.get("CLOUDINARY_CLOUD_NAME"),
        api_key=app.config.get("CLOUDINARY_API_KEY"),
        api_secret=app.config.get("CLOUDINARY_API_SECRET"),
        secure=True,
    )

    db.init_app(app)
    oauth.init_app(app)

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(mentors_bp)

    with app.app_context():
        db.create_all()

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
