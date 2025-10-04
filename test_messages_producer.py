import json
import os
import random
import time
from typing import Any, Dict

import pika
from confluent_kafka import Producer


def generate_message(message_id: int) -> Dict[str, Any]:
    texts = [
        "Hello from the queue!",
        "Testing message processing",
        "Random text content",
        "Queue reader test message",
        "Sample data for testing",
    ]

    return {
        "Id": message_id,
        "Body": random.choice(texts),
        "Metrics": {"Likes": random.randint(0, 100), "Views": random.randint(0, 1000)},
    }


def produce_to_kafka(bootstrap_servers: str, topic: str, count: int = 50):
    try:
        conf = {"bootstrap.servers": bootstrap_servers}
        producer = Producer(conf)

        def delivery_callback(err, msg):
            if err:
                print(f"Ошибка доставки: {err}")

        for i in range(1, count + 1):
            message = generate_message(i)
            producer.produce(
                topic, key=str(i), value=json.dumps(message), callback=delivery_callback
            )
            if i % 10 == 0:
                producer.flush()

        print(f"✓ Успешно отправлено {count} сообщений в Kafka")

    except Exception as e:
        print(f"Ошибка при отправке в Kafka: {e}")


def produce_to_rabbitmq(host: str, queue: str, count: int = 50):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
        channel = connection.channel()

        channel.queue_declare(queue=queue, durable=True)

        print(f"Отправка {count} сообщений в RabbitMQ очередь: {queue}")

        for i in range(1, count + 1):
            message = generate_message(i)
            channel.basic_publish(
                exchange="",
                routing_key=queue,
                body=json.dumps(message),
                properties=pika.BasicProperties(
                    delivery_mode=2,
                ),
            )

            if i % 10 == 0:
                print(f"Отправлено {i} сообщений в RabbitMQ")

        connection.close()
        print(f"✓ Успешно отправлено {count} сообщений в RabbitMQ")

    except Exception as e:
        print(f"Ошибка при отправке в RabbitMQ: {e}")


def main():
    kafka_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
    rabbitmq_host = os.getenv("RABBITMQ_HOST")

    kafka_topic = "test_topic"
    rabbitmq_queue = "test_queue"
    messages_count = 50

    print("=" * 60)
    print("Генератор тестовых сообщений")
    print("=" * 60)

    print("\n--- Kafka ---")
    produce_to_kafka(kafka_servers, kafka_topic, messages_count)

    time.sleep(2)

    print("\n--- RabbitMQ ---")
    produce_to_rabbitmq(rabbitmq_host, rabbitmq_queue, messages_count)

    print("\n" + "=" * 60)
    print("✓ Тестовые данные сгенерированы!")
    print("=" * 60)
    print("\nТеперь можно использовать приложение:")
    print(
        f"  Kafka:    queuereader read {kafka_servers} {kafka_topic} -skip 0 -take 10 -o output.txt -t kafka"
    )
    print(
        f"  RabbitMQ: queuereader read {rabbitmq_host} {rabbitmq_queue} -skip 0 -take 10 -o output.txt -t rabbitmq"
    )


if __name__ == "__main__":
    main()
