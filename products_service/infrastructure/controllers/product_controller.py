import os
import pika
import json
from flask import jsonify
from products_service.application.product_use_case import ProductUseCase
from products_service.domain.product_repository import ProductRepository
from products_service.infrastructure.database import get_database
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
RABBITMQ_USER = os.getenv("RABBITMQ_USER")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD")
RABBITMQ_PRODUCT_QUEUE = os.getenv("RABBITMQ_PRODUCT_QUEUE")


class ProductController:
    def __init__(self):
        database = get_database()
        self.product_use_case = ProductUseCase(ProductRepository(database))

    def publish_to_queue(self, message):
        try:
            print(f"[DEBUG] Conectando a RabbitMQ en {RABBITMQ_HOST}...")
            # Configuración de credenciales y conexión
            credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials)
            )
            print("[DEBUG] Conexión establecida con RabbitMQ.")
            channel = connection.channel()

            # Declarar la cola (asegurarse de que es durable)
            channel.queue_declare(queue=RABBITMQ_PRODUCT_QUEUE, durable=True)
            print(f"[DEBUG] Cola '{RABBITMQ_PRODUCT_QUEUE}' declarada exitosamente.")

            # Publicar el mensaje en la cola
            channel.basic_publish(
                exchange='',
                routing_key=RABBITMQ_PRODUCT_QUEUE,
                body=json.dumps(message),  # Serializar el mensaje como JSON
                properties=pika.BasicProperties(
                    delivery_mode=2  # Persistencia del mensaje
                )
            )
            print(f"[SUCCESS] Mensaje publicado en la cola '{RABBITMQ_PRODUCT_QUEUE}': {message}")
        except pika.exceptions.AMQPConnectionError as conn_err:
            print(f"[ERROR] Error de conexión con RabbitMQ: {conn_err}")
        except Exception as e:
            print(f"[ERROR] Error publicando mensaje: {e}")
        finally:
            # Cerrar la conexión de RabbitMQ
            try:
                if 'connection' in locals() and connection and not connection.is_closed:
                    print("[DEBUG] Cerrando conexión con RabbitMQ...")
                    connection.close()
                    print("[DEBUG] Conexión cerrada correctamente.")
            except Exception as e:
                print(f"[ERROR] Error cerrando conexión: {e}")

    def get_all_products(self):
        try:
            print("[DEBUG] Obteniendo todos los productos...")
            products = self.product_use_case.get_all_products()
            return jsonify(products), 200
        except Exception as e:
            print(f"[ERROR] Error obteniendo productos: {e}")
            return jsonify({"error": str(e)}), 500

    def add_product(self, data):
        try:
            print("[DEBUG] Añadiendo producto a la base de datos...")
            # Añadir el producto a la base de datos
            new_product = self.product_use_case.add_product(data)
            print(f"[DEBUG] Producto añadido: {new_product}")

            # Publicar el producto en RabbitMQ
            self.publish_to_queue({
                "operation": "create",
                "data": new_product
            })

            return jsonify({"message": "Product created", "product": new_product}), 201
        except Exception as e:
            print(f"[ERROR] Error al crear producto: {e}")
            return jsonify({"error": str(e)}), 500
