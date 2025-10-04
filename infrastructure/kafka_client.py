import json
import uuid

from confluent_kafka import Consumer, KafkaError
from domain.models import Message
from infrastructure.base_client import BaseClient


class KafkaClient(BaseClient):
    def __init__(self, bootstrap_servers: str, timeout_ms: int = 5000):
        self.bootstrap_servers = bootstrap_servers
        self.timeout_ms = timeout_ms
        self.timeout_seconds = timeout_ms / 1000.0
        conf = {
            "bootstrap.servers": self.bootstrap_servers,
            "group.id": f"queue-reader-{uuid.uuid4()}",
            "auto.offset.reset": "earliest",
            "enable.auto.commit": False,
            "fetch.min.bytes": 512,
            "fetch.wait.max.ms": 100,
            "max.partition.fetch.bytes": 2097152,
            "queued.min.messages": 100000,
        }
        self.consumer = Consumer(conf)

    def connect(self) -> None:
        pass

    def read_messages(self, topic_name: str, count: int) -> list[Message]:
        messages = []

        self.consumer.subscribe([topic_name])

        while len(messages) < count:
            msg = self.consumer.poll(timeout=self.timeout_seconds)

            if msg is None:
                continue

            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    break
                else:
                    print(f"Ошибка Kafka: {msg.error()}")
                    continue

            try:
                message_value = json.loads(msg.value().decode("utf-8"))
                message = Message.from_dict(message_value)
                messages.append(message)
            except (json.JSONDecodeError, UnicodeDecodeError) as e:
                print(f"Ошибка декодирования сообщения: {e}")
                continue

        return messages

    def close(self) -> None:
        if self.consumer:
            self.consumer.close()
