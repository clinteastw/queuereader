import argparse
import sys


class CLI:
    @staticmethod
    def parse_args() -> argparse.Namespace:
        parser = argparse.ArgumentParser(
            description="Читает сообщения из RabbitMQ или Kafka с пейджингом"
        )

        parser.add_argument("command", choices=["read"], help="Команда для выполнения")

        parser.add_argument(
            "server", help="Адрес сервера (kafka-bootstrap или rabbitmq-host)"
        )

        parser.add_argument("queue_name", help="Имя очереди или топика")

        parser.add_argument(
            "-skip",
            type=int,
            default=0,
            help="Количество сообщений для пропуска (по умолчанию: 0)",
        )

        parser.add_argument(
            "-take",
            type=int,
            default=10,
            help="Количество сообщений для чтения (по умолчанию: 10)",
        )

        parser.add_argument("-o", "--output", required=True, help="Имя выходного файла")

        parser.add_argument(
            "-t",
            "--type",
            choices=["kafka", "rabbitmq"],
            default="kafka",
            help="Тип очереди (по умолчанию: kafka)",
        )

        return parser.parse_args()

    @staticmethod
    def validate_args(args: argparse.Namespace) -> None:
        """Валидирует аргументы"""
        if args.skip < 0:
            print("Ошибка: -skip должен быть >= 0", file=sys.stderr)
            sys.exit(1)

        if args.take <= 0:
            print("Ошибка: -take должен быть > 0", file=sys.stderr)
            sys.exit(1)
