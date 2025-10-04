# Запуск

```
cd queuereader
docker-compose up --build -d
```
### Добавить сообщения в Kafka и RabbitMQ
```
docker exec -it queuereader-app python test_messages_producer.py
```
### Прочитать сообщения из Kafka
```
docker exec -it queuereader-app queuereader read kafka:9093 test_topic -skip 0 -take 10 -o kafka.txt -t kafka
```
### Прочитать сообщения из RabbitMQ
```
docker exec -it queuereader-app queuereader read rabbitmq:5672 test_queue -skip 0 -take 10 -o rabbitmq.txt -t rabbitmq
```
### Просмотреть сохраненные сообщения
```
docker exec -it queuereader-app cat kafka.txt
docker exec -it queuereader-app cat rabbitmq.txt
```
