import os
import pika

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")

def publicar_rabbitmq(pedido_id: str):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
        channel = connection.channel()
        channel.queue_declare(queue='fila_pedidos', durable=True)
        
        mensagem = f"Pedido criado: {pedido_id}"
        
        channel.basic_publish(
            exchange='',
            routing_key='fila_pedidos',
            body=mensagem
        )
        connection.close()
    except Exception as e:
        print(f"Erro ao publicar no RabbitMQ: {e}")