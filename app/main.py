import uuid
from typing import List
from fastapi import FastAPI, status
from pydantic import BaseModel, Field
from app.database import colecao_pedidos
from app.mensageriaRabbit import publicar_rabbitmq
from app.mensageriaKafka import publicar_kafka

app = FastAPI(title="API de Gerenciamento de Pedidos")

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
    
    publicar_rabbitmq(pedido_id)
    publicar_kafka(pedido_id, pedido.nome_cliente)
    
    return novo_pedido

@app.get("/pedidos", response_model=List[PedidoResponse], status_code=status.HTTP_200_OK)
async def listar_pedidos():
    pedidos_cursor = colecao_pedidos.find()
    pedidos = await pedidos_cursor.to_list(length=100)
    return pedidos