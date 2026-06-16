import os
import confluent_kafka

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")

def publicar_kafka(pedido_id: str, nome_cliente: str):
    try:
        conf = {'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS}
        producer = confluent_kafka.Producer(conf)
        
        evento = f"Evento: Pedido {pedido_id} criado para o cliente {nome_cliente}"
        
        producer.produce('pedidos_topico', value=evento.encode('utf-8'))
        producer.flush()
    except Exception as e:
        print(f"Erro ao publicar no Kafka: {e}")