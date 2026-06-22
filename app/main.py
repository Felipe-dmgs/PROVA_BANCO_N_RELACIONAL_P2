import uuid
from typing import List
from contextlib import asynccontextmanager
from fastapi import FastAPI, status
from pydantic import BaseModel, Field
from app.database import colecao_pedidos
from app.mensageriaRabbit import RabbitMQService
from app.mensageriaKafka import KafkaService
import os

RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/")
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
rabbitmq_service = RabbitMQService(url=RABBITMQ_URL, queue_name="fila_pedidos")
kafka_service = KafkaService(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS, topic="pedidos_topico")

@asynccontextmanager
async def lifespan(app: FastAPI):
    await rabbitmq_service.connect()
    await kafka_service.connect()

    yield

    await rabbitmq_service.close()
    await kafka_service.close()

app = FastAPI(title="API de Gerenciamento de Pedidos", lifespan=lifespan)

class PedidoCreate(BaseModel):
    nome_cliente: str
    nome_produto: str
    quantidade: int

class PedidoResponse(PedidoCreate):
    id: str = Field(..., alias="_id")
    status: str = "PENDENTE"

@app.post("/pedidos", response_model=PedidoResponse, status_code=status.HTTP_201_CREATED)
async def cadastrar_pedido(pedido: PedidoCreate):
    pedido_id = str(uuid.uuid4())
    novo_pedido = pedido.model_dump()
    novo_pedido["_id"] = pedido_id
    novo_pedido["status"] = "PENDENTE"
    
    await colecao_pedidos.insert_one(novo_pedido)
    
    msg_rabbit = f"Pedido criado: {pedido_id}"
    msg_kafka = f"Evento: Pedido {pedido_id} criado para o cliente {pedido.nome_cliente}"
    
    await rabbitmq_service.publish(msg_rabbit)
    await kafka_service.publish(key=pedido_id, message=msg_kafka)
    
    return novo_pedido

@app.get("/pedidos", response_model=List[PedidoResponse], status_code=status.HTTP_200_OK)
async def listar_pedidos():
    pedidos_cursor = colecao_pedidos.find()
    pedidos = await pedidos_cursor.to_list(length=100)
    return pedidos