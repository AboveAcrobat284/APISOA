from flask import Blueprint, request
from users_service.infrastructure.controllers.user_controller import UserController
from flask import Blueprint, jsonify

user_routes = Blueprint("user_routes", __name__)
user_controller = UserController()

@user_routes.route("/users", methods=["GET", "POST"])
def users():
    if request.method == "GET":
        return user_controller.get_all_users()
    elif request.method == "POST":
        return user_controller.add_user(request.json)

@user_routes.route("/health", methods=["GET"])
def health_check():
    try:
        return jsonify({"status": "ok", "service": "users_service"}), 200
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500
