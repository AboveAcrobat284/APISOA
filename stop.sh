#!/bin/bash

echo "========== Deteniendo Servicios =========="

# Detener procesos Python para API y consumidores
echo "Deteniendo servicios Python..."
pkill -f "python app.py" || echo "No se encontraron procesos de API ejecutándose."
pkill -f "python infrastructure/rabbitmq_consumer.py" || echo "No se encontraron consumidores de RabbitMQ ejecutándose."

# Detener RabbitMQ
echo "Deteniendo RabbitMQ..."
if [ "$(docker ps -q -f name=rabbitmq)" ]; then
  docker stop rabbitmq && echo "RabbitMQ detenido." || echo "Error al detener RabbitMQ."
else
  echo "RabbitMQ ya estaba detenido."
fi

echo "========== Servicios Detenidos =========="
