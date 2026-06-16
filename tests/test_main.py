import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from app.main import app

client = TestClient(app)

@patch('app.main.publicar_rabbitmq')
@patch('app.main.publicar_kafka')
@patch('app.main.colecao_pedidos.insert_one', new_callable=AsyncMock)
def test_cadastrar_pedido(mock_insert, mock_kafka, mock_rabbit):
    payload = {
        "nome_cliente": "Anderson Felipe",
        "nome_produto": "Monitor Ultrawide",
        "quantidade": 1
    }
    
    response = client.post("/pedidos", json=payload)
    
    assert response.status_code == 201
    dados = response.json()
    assert dados["nome_cliente"] == payload["nome_cliente"]
    assert dados["status"] == "PENDENTE"
    assert "_id" in dados 
    assert mock_insert.called
    assert mock_rabbit.called
    assert mock_kafka.called

@patch('app.main.colecao_pedidos.find')
def test_listar_pedidos(mock_find):
    mock_cursor = AsyncMock()
    mock_cursor.to_list.return_value = [
        {
            "_id": "id-falso-123",
            "nome_cliente": "Anderson Felipe",
            "nome_produto": "Monitor Ultrawide",
            "quantidade": 1,
            "status": "PENDENTE"
        }
    ]
    mock_find.return_value = mock_cursor
    response = client.get("/pedidos")
    assert response.status_code == 200
    dados = response.json()
    assert isinstance(dados, list)
    assert len(dados) > 0
    assert dados[0]["_id"] == "id-falso-123"