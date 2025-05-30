from flask import Blueprint

home_bp = Blueprint("home", __name__, url_prefix="/home")


@home_bp.route("/")
def home():
    return "Hello!"
