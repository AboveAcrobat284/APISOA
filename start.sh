#!/bin/bash
# Configuración global de PYTHONPATH
export PYTHONPATH=$(pwd)
LOG_DIR=logs
mkdir -p $LOG_DIR

echo "========== Iniciando RabbitMQ =========="
if [ "$(docker ps -q -f name=rabbitmq)" ]; then
  echo "RabbitMQ ya está corriendo."
else
  echo "Iniciando RabbitMQ..."
  docker start rabbitmq || { echo "Error iniciando RabbitMQ. Asegúrate de que esté configurado."; exit 1; }
fi

echo "========== Iniciando Servicio de Usuarios =========="
(
  cd users_service || exit
  export PYTHONPATH=$PYTHONPATH:$(pwd)
  echo "Iniciando consumidor de RabbitMQ para Usuarios..."
  nohup python -m infrastructure.rabbitmq_consumer >> "../$LOG_DIR/users_consumer.log" 2>&1 &
  sleep 2  # Permitir que el consumidor inicie
  echo "Iniciando API de Usuarios..."
  nohup python app.py >> "../$LOG_DIR/users_api.log" 2>&1 &
  sleep 2
  # Validar si el puerto está en uso
  if lsof -i :5001 > /dev/null; then
    echo "Servicio de Usuarios iniciado correctamente en el puerto 5001."
  else
    echo "Error: El servicio de Usuarios no está escuchando en el puerto 5001."
  fi
)

echo "========== Iniciando Servicio de Productos =========="
(
  cd products_service || exit
  export PYTHONPATH=$PYTHONPATH:$(pwd)
  echo "Iniciando consumidor de RabbitMQ para Productos..."
  nohup python -m infrastructure.rabbitmq_consumer >> "../$LOG_DIR/products_consumer.log" 2>&1 &
  sleep 2  # Permitir que el consumidor inicie
  echo "Iniciando API de Productos..."
  nohup python app.py >> "../$LOG_DIR/products_api.log" 2>&1 &
  sleep 2
  # Validar si el puerto está en uso
  if lsof -i :5002 > /dev/null; then
    echo "Servicio de Productos iniciado correctamente en el puerto 5002."
  else
    echo "Error: El servicio de Productos no está escuchando en el puerto 5002."
  fi
)

echo "========== Iniciando API Gateway =========="
(
  cd gateway || exit
  export PYTHONPATH=$PYTHONPATH:$(pwd)
  echo "Iniciando API Gateway..."
  nohup python app.py >> "../$LOG_DIR/gateway.log" 2>&1 &
  sleep 2
  # Validar si el puerto está en uso
  if lsof -i :5000 > /dev/null; then
    echo "Gateway iniciado correctamente en el puerto 5000."
  else
    echo "Error: El Gateway no está escuchando en el puerto 5000."
  fi
)

echo "========== Sistema Iniciado =========="
echo "Logs disponibles en el directorio '$LOG_DIR'."
