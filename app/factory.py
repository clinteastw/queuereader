from infrastructure.base_client import BaseClient
from infrastructure.kafka_client import KafkaClient
from infrastructure.rabbitmq_client import RabbitMQClient


class QueueClientFactory:
    @staticmethod
    def create(queue_type: str, server: str, **kwargs) -> BaseClient:
        if queue_type == "kafka":
            return KafkaClient(server, **kwargs)
        elif queue_type == "rabbitmq":
            host = server.split(":")[0]
            port = int(server.split(":")[1]) if ":" in server else 5672
            username = kwargs.get("username", "guest")
            password = kwargs.get("password", "guest")
            return RabbitMQClient(host, port, username, password)
        else:
            raise ValueError(f"Неизвестный тип очереди: {queue_type}")
