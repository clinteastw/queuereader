import json

from domain.models import Message
from infrastructure.base_client import BaseClient
from pika import BlockingConnection, ConnectionParameters, PlainCredentials


class RabbitMQClient(BaseClient):
    def __init__(
        self,
        host: str,
        port: int = 5672,
        username: str = "guest",
        password: str = "guest",
    ):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.connection = None
        self.channel = None

    def connect(self) -> None:
        credentials = PlainCredentials(self.username, self.password)
        parameters = ConnectionParameters(
            host=self.host, port=self.port, credentials=credentials
        )
        self.connection = BlockingConnection(parameters)
        self.channel = self.connection.channel()

    def read_messages(self, queue_name: str, count: int) -> list[Message]:
        if not self.channel:
            self.connect()

        self.channel.queue_declare(queue=queue_name, passive=True)
        messages = []

        for _ in range(count):
            method_frame, header_frame, body = self.channel.basic_get(queue_name)

            if method_frame is None:
                break

            try:
                message_data = json.loads(body.decode("utf-8"))
                message = Message.from_dict(message_data)
                messages.append(message)
                self.channel.basic_ack(method_frame.delivery_tag)
            except json.JSONDecodeError:
                continue

        return messages

    def close(self) -> None:
        if self.connection:
            self.connection.close()
