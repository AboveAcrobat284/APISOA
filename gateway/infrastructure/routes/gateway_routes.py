from flask import Blueprint, jsonify, request
import requests

gateway_routes = Blueprint("gateway_routes", __name__)

USERS_SERVICE_URL = "http://localhost:5001"
PRODUCTS_SERVICE_URL = "http://localhost:5002"

@gateway_routes.route("/health", methods=["GET"])
def health_check():
    try:
        users_health = requests.get(f"{USERS_SERVICE_URL}/health", timeout=5)
        users_status = users_health.json() if users_health.status_code == 200 else {"status": "error"}
        
        products_health = requests.get(f"{PRODUCTS_SERVICE_URL}/health", timeout=5)
        products_status = products_health.json() if products_health.status_code == 200 else {"status": "error"}

        return jsonify({
            "gateway": {"status": "ok", "service": "gateway"},
            "users_service": users_status,
            "products_service": products_status
        }), 200
    except Exception as e:
        return jsonify({
            "gateway": {"status": "error", "error": str(e)},
            "users_service": {"status": "unknown"},
            "products_service": {"status": "unknown"}
        }), 500

@gateway_routes.route("/users", methods=["GET", "POST"])
def users_proxy():
    if request.method == "GET":
        response = requests.get(f"{USERS_SERVICE_URL}/users")
    elif request.method == "POST":
        response = requests.post(f"{USERS_SERVICE_URL}/users", json=request.json)
    return jsonify(response.json()), response.status_code

@gateway_routes.route("/products", methods=["GET", "POST"])
def products_proxy():
    if request.method == "GET":
        response = requests.get(f"{PRODUCTS_SERVICE_URL}/products")
    elif request.method == "POST":
        response = requests.post(f"{PRODUCTS_SERVICE_URL}/products", json=request.json)
    return jsonify(response.json()), response.status_code
