from flask import Blueprint, request
from flask import Blueprint, jsonify
from products_service.infrastructure.controllers.product_controller import ProductController

product_routes = Blueprint("product_routes", __name__)
product_controller = ProductController()

@product_routes.route("/products", methods=["GET", "POST"])
def products():
    if request.method == "GET":
        return product_controller.get_all_products()
    elif request.method == "POST":
        return product_controller.add_product(request.json)

@product_routes.route("/health", methods=["GET"])
def health_check():
    try:
        return jsonify({"status": "ok", "service": "products_service"}), 200
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500
