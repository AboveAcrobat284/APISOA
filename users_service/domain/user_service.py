class UserService:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    def get_all_users(self):
        return self.user_repository.get_all_users()

    def add_user(self, user_data):
        return self.user_repository.add_user(user_data)
