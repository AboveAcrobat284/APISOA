import uuid

class UserRepository:
    def __init__(self, database):
        self.collection = database["users"]

    def add_user(self, user_data):
        # Generar un UUID para el nuevo usuario
        user_data["_id"] = str(uuid.uuid4())  # Asignar un UUID como _id
        self.collection.insert_one(user_data)
        return user_data

    def get_all_users(self):
        # Recuperar todos los usuarios
        users = self.collection.find()
        return list(users)  # Devolver como lista, UUID ya está serializable
