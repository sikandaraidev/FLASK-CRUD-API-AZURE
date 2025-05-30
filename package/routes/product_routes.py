# app/routes/product_routes.py

from flask import Blueprint, jsonify, request

from package.azure_database import get_session
from package.models.product_model import Product
from package.schemas.product_schema import ProductSchema

product_bp = Blueprint("product", __name__, url_prefix="/products")


@product_bp.route("/", methods=["GET"])
def get_products():
    session = next(get_session())
    category = request.args.get("category")
    query = session.query(Product)
    if category:
        query = query.filter(Product.category == category)
    products = query.all()
    return jsonify([product for product in products])


@product_bp.route("/<int:product_id>", methods=["GET"])
def get_product(product_id):
    session = next(get_session())
    product = session.get(Product, product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(product.to_dict())


@product_bp.route("/", methods=["POST"])
def create_product():
    session = next(get_session())
    product_schema = ProductSchema()
    data = product_schema.load(request.json)
    product = Product(**data)
    session.add(product)
    session.commit()
    product_schema = ProductSchema()
    return product_schema.dump(product), 201


@product_bp.route("/<int:product_id>", methods=["PATCH"])
def update_product(product_id):
    session = next(get_session())
    product = session.get(Product, product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    data = request.json
    for key, value in data.items():
        setattr(product, key, value)
    session.commit()
    return jsonify(product.to_dict())


@product_bp.route("/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    session = next(get_session())
    product = session.get(Product, product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    session.delete(product)
    session.commit()
    return jsonify({"message": "Product deleted"})
