from flask import Flask
from gateway.infrastructure.routes.gateway_routes import gateway_routes

app = Flask(__name__)
app.register_blueprint(gateway_routes)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
