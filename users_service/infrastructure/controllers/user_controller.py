import os
import pika
from dotenv import load_dotenv
from flask import jsonify
from users_service.application.user_use_case import UserUseCase
from users_service.domain.user_repository import UserRepository
from users_service.infrastructure.database import get_database

# Cargar variables de entorno
load_dotenv()

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
RABBITMQ_USER = os.getenv("RABBITMQ_USER")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD")
RABBITMQ_USER_QUEUE = os.getenv("RABBITMQ_USER_QUEUE")

class UserController:
    def __init__(self):
        database = get_database()
        self.user_use_case = UserUseCase(UserRepository(database))

    def publish_to_queue(self, message):
        credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials))
        channel = connection.channel()
        channel.queue_declare(queue=RABBITMQ_USER_QUEUE, durable=True)
        channel.basic_publish(exchange='', routing_key=RABBITMQ_USER_QUEUE, body=str(message))
        connection.close()

    def get_all_users(self):
        try:
            users = self.user_use_case.get_all_users()
            return jsonify(users), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def add_user(self, data):
        try:
            new_user = self.user_use_case.add_user(data)
            self.publish_to_queue({"operation": "create", "data": new_user})
            return jsonify({"message": "User created", "user": new_user}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500
