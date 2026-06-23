# API de Gerenciamento de Pedidos (FastAPI + MongoDB + RabbitMQ + Kafka)

Este projeto foi desenvolvido como parte da avaliação de Banco de Dados Não Relacional (P2). A aplicação consiste em uma API assíncrona para gerenciamento de pedidos, integrando persistência em banco NoSQL e mensageria distribuída de alta performance.

## 🚀 Arquitetura e Tecnologias

- **Framework:** FastAPI (Python 3.14+)
- **Banco de Dados:** MongoDB (utilizando o driver assíncrono `motor`)
- **Mensageria & Eventos:** - **RabbitMQ:** Publicação assíncrona de mensagens utilizando `aio-pika`.
  - **Apache Kafka:** Publicação assíncrona de eventos utilizando `aiokafka` (com suporte a Zookeeper na versão estável 7.4.4).
- **Testes & Cobertura:** Pytest + Pytest-Cov com isolamento de infraestrutura via `AsyncMock`.
- **Conteinerização:** Docker & Docker Compose para orquestração de todo o ecossistema.

## 🛠️ Como Executar o Projeto

Certifique-se de ter o **Docker** e o **Docker Compose** instalados em sua máquina.

### 1. Clonar o projeto e configurar o ambiente
Certifique-se de que o arquivo `.env` está presente na raiz com as seguintes variáveis de ambiente apontando para a rede interna do Docker:
```env
MONGO_URL=mongodb://mongodb:27017
RABBITMQ_URL=amqp://guest:guest@rabbitmq:5672/
KAFKA_BOOTSTRAP_SERVERS=kafka:29092
```
### 2. Para testar esse projeto primeiro temos que subir o compose com 
```
    docker compose up -d
```
### 3. Para rodar os testes
```
    python -m pytest -v --cov=app --cov-report=term-missing
```
### 4. Encerrar o ambiente
```
    docker compose down
```