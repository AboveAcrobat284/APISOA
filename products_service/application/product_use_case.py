import uuid

class ProductUseCase:
    def __init__(self, product_repository):
        self.product_repository = product_repository

    def get_all_products(self):
        return self.product_repository.get_all_products()

    def add_product(self, product_data):
        product_data["id"] = str(uuid.uuid4())
        return self.product_repository.add_product(product_data)
