import os
import pika
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
RABBITMQ_USER = os.getenv("RABBITMQ_USER")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD")
RABBITMQ_PRODUCT_QUEUE = os.getenv("RABBITMQ_PRODUCT_QUEUE")

def callback(ch, method, properties, body):
    print(f" [x] Recibido mensaje en la cola '{RABBITMQ_PRODUCT_QUEUE}': {body}")
    # Aquí puedes procesar el mensaje según sea necesario
    ch.basic_ack(delivery_tag=method.delivery_tag)

def start_product_consumer():
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials))
    channel = connection.channel()

    # Declarar la cola (durable=True para persistencia)
    channel.queue_declare(queue=RABBITMQ_PRODUCT_QUEUE, durable=True)

    print(f" [*] Esperando mensajes en la cola '{RABBITMQ_PRODUCT_QUEUE}'. Presiona CTRL+C para salir.")
    channel.basic_consume(queue=RABBITMQ_PRODUCT_QUEUE, on_message_callback=callback)

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print(" [x] Consumidor detenido.")
    except pika.exceptions.ConnectionClosedByBroker:
        print(" [x] Conexión cerrada por el broker.")
    except Exception as e:
        print(f" [x] Error inesperado: {e}")
    finally:
        if not connection.is_closed:
            connection.close()

if __name__ == "__main__":
    start_product_consumer()
