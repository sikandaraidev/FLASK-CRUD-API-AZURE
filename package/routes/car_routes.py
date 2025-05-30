# package/routes/car_routes.py
from flask import Blueprint, jsonify, request

from package.azure_database import get_session
from package.models.car_model import Car

car_bp = Blueprint("car", __name__, url_prefix="/cars")


@car_bp.route("/", methods=["GET"])
def get_cars():
    session = next(get_session())
    brand = request.args.get("brand")
    query = session.query(Car)
    if brand:
        query = query.filter(Car.brand == brand)
    cars = query.all()
    return jsonify([car.to_dict() for car in cars])


@car_bp.route("/<int:car_id>", methods=["GET"])
def get_car(car_id):
    session = next(get_session())
    car = session.get(Car, car_id)
    if not car:
        return jsonify({"error": "Car not found"}), 404
    return jsonify(car.to_dict())


@car_bp.route("/", methods=["POST"])
def create_car():
    session = next(get_session())
    data = request.json
    car = Car(**data)
    session.add(car)
    session.commit()
    return jsonify(car.to_dict()), 201


@car_bp.route("/<int:car_id>", methods=["PATCH"])
def update_car(car_id):
    session = next(get_session())
    car = session.get(Car, car_id)
    if not car:
        return jsonify({"error": "Car not found"}), 404
    data = request.json
    for key, value in data.items():
        setattr(car, key, value)
    session.commit()
    return jsonify(car.to_dict())


@car_bp.route("/<int:car_id>", methods=["DELETE"])
def delete_car(car_id):
    session = next(get_session())
    car = session.get(Car, car_id)
    if not car:
        return jsonify({"error": "Car not found"}), 404
    session.delete(car)
    session.commit()
    return jsonify({"message": "Car deleted"})
