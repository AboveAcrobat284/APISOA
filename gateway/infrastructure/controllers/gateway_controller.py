from flask import jsonify, request
from gateway.application.gateway_service import GatewayService
from gateway.domain.gateway_logic import GatewayLogic

class GatewayController:
    def __init__(self):
        self.gateway_service = GatewayService(GatewayLogic())

    def process_request(self):
        try:
            data = request.json
            response = self.gateway_service.handle_request(data)
            return jsonify(response), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
