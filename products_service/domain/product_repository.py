import uuid

class ProductRepository:
    def __init__(self, database):
        self.collection = database["products"]

    def add_product(self, product_data):
        # Generar un UUID para el nuevo producto
        product_data["_id"] = str(uuid.uuid4())  # Asignar un UUID como _id
        self.collection.insert_one(product_data)
        return product_data

    def get_all_products(self):
        # Recuperar todos los productos
        products = self.collection.find()
        return list(products)  # Devolver como lista, UUID ya está serializable
