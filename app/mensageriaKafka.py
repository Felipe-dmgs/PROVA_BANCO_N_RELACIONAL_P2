import asyncio
import logging
from aiokafka import AIOKafkaProducer

logger = logging.getLogger(__name__)

class KafkaService:
    def __init__(self, bootstrap_servers: str, topic: str):
        self.bootstrap_servers = bootstrap_servers
        self.topic = topic
        self.producer = None

    async def connect(self):
        while True:
            try:
                self.producer = AIOKafkaProducer(bootstrap_servers=self.bootstrap_servers)
                await self.producer.start()
                logger.info("Conectado ao Kafka com sucesso!")
                break
            except Exception as e:
                logger.warning(f"Kafka indisponível. Tentando novamente em 3s... Erro: {e}")
                await asyncio.sleep(3)

    async def publish(self, key: str, message: str):
        if not self.producer:
            await self.connect()
            
        await self.producer.send_and_wait(
            topic=self.topic,
            key=key.encode("utf-8"),
            value=message.encode("utf-8")
        )

    async def close(self):
        if self.producer:
            await self.producer.stop() 