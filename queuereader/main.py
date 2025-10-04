import sys

from app.factory import QueueClientFactory
from app.services import QueueReaderService
from config.settings import get_settings
from dotenv import load_dotenv
from infrastructure.file_storage import FileStorage
from presentation.cli import CLI


def main():
    load_dotenv()

    settings = get_settings()

    cli = CLI()
    args = cli.parse_args()
    cli.validate_args(args)

    try:
        print(f"Чтение из {args.type}: {args.server}")
        print(f"Очередь/топик: {args.queue_name}")
        print(f"Пропуск: {args.skip}, Чтение: {args.take}")

        if args.type == "rabbitmq":
            client = QueueClientFactory.create(
                args.type,
                args.server,
                username=settings.rabbitmq_user,
                password=settings.rabbitmq_password,
            )
        else:
            client = QueueClientFactory.create(args.type, args.server)

        storage = FileStorage()
        service = QueueReaderService(client, storage)

        count = service.read_and_save(
            args.queue_name, args.skip, args.take, args.output
        )
        if not count:
            print(f"В очереди: {args.queue_name} нет сообщений")
            return

        print(f"✓ Сохранено {count} сообщений в файл: {args.output}")

    except Exception as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
