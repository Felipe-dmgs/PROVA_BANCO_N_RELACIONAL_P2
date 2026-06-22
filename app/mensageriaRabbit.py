import asyncio
import logging
import aio_pika

logger = logging.getLogger(__name__)

class RabbitMQService:
    def __init__(self, url: str, queue_name: str):
        self.url = url
        self.queue_name = queue_name
        self.connection = None
        self.channel = None

    async def connect(self):
        while True:
            try:
                self.connection = await aio_pika.connect_robust(self.url)
                self.channel = await self.connection.channel()
                await self.channel.declare_queue(self.queue_name, durable=True)
                logger.info("Conectado ao RabbitMQ com sucesso!")
                break
            except Exception as e:
                logger.warning(f"RabbitMQ indisponível. Tentando novamente em 3s... Erro: {e}")
                await asyncio.sleep(3)

    async def publish(self, message: str):
        if not self.channel:
            await self.connect()
            
        await self.channel.default_exchange.publish(
            aio_pika.Message(
                body=message.encode("utf-8"),
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT
            ),
            routing_key=self.queue_name,
        )

    async def close(self):
        if self.connection:
            await self.connection.close()