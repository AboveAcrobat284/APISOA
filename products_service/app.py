from flask import Flask
from products_service.infrastructure.routes.product_routes import product_routes

app = Flask(__name__)
app.register_blueprint(product_routes)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
