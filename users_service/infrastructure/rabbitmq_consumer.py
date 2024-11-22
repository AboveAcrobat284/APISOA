import os
import pika
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
RABBITMQ_USER = os.getenv("RABBITMQ_USER")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD")
RABBITMQ_USER_QUEUE = os.getenv("RABBITMQ_USER_QUEUE")

def callback(ch, method, properties, body):
    print(f" [x] Recibido mensaje en la cola '{RABBITMQ_USER_QUEUE}': {body}")

def start_user_consumer():
    # Configurar credenciales
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials))
    channel = connection.channel()

    # Declarar la cola (durable=True para persistencia)
    channel.queue_declare(queue=RABBITMQ_USER_QUEUE, durable=True)

    # Configurar consumidor
    channel.basic_consume(queue=RABBITMQ_USER_QUEUE, on_message_callback=callback, auto_ack=True)

    print(f" [*] Esperando mensajes en la cola '{RABBITMQ_USER_QUEUE}'. Presiona CTRL+C para salir.")
    channel.start_consuming()

if __name__ == "__main__":
    try:
        start_user_consumer()
    except KeyboardInterrupt:
        print("\n [!] Consumidor de usuarios detenido.")
