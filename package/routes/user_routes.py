# app/routes/user_routes.py
from flask import Blueprint, jsonify, request

from package.azure_database import get_session
from package.models.user_model import User
from package.schemas.user_schema import UserSchema

user_bp = Blueprint("user", __name__, url_prefix="/users")


@user_bp.route("/", methods=["GET"])
def get_users():
    session = next(get_session())
    users = session.query(User).all()
    user_schema = UserSchema(many=True)
    return user_schema.dump(users), 201


@user_bp.route("/<int:user_id>", methods=["GET"])
def get_user(user_id):
    session = next(get_session())
    user = session.query(User).get(user_id)
    if user is None:
        return jsonify({"error": "User not found"}), 404
    user_schema = UserSchema()
    return user_schema.dump(user), 201


@user_bp.route("/", methods=["POST"])
def create_user():
    data = request.json
    session = next(get_session())
    user = User(**data)
    session.add(user)
    session.commit()
    user_schema = UserSchema()
    return user_schema.dump(user), 201
    # return jsonify(user.to_dict()), 201


@user_bp.route("/<int:user_id>", methods=["PUT"])
def update_user_complete(user_id):
    session = next(get_session())
    user = session.query(User).get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    data = request.json
    for key, value in data.items():
        setattr(user, key, value)
    session.commit()
    user_schema = UserSchema()
    return user_schema.dump(user), 201


@user_bp.route("/<int:user_id>", methods=["PATCH"])
def update_user(user_id):
    session = next(get_session())
    user = session.query(User).get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    data = request.json
    for key, value in data.items():
        setattr(user, key, value)
    session.commit()
    user_schema = UserSchema()
    return user_schema.dump(user), 201


@user_bp.route("/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    session = next(get_session())
    user = session.get(User, user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    session.delete(user)
    session.commit()
    return jsonify({"message": "User deleted"})
