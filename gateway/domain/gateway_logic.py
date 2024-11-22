class GatewayService:
    def __init__(self, logic):
        self.logic = logic

    def handle_request(self, data):
        return self.logic.process_request(data)
