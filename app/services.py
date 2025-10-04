from infrastructure.base_client import BaseClient
from infrastructure.file_storage import FileStorage


class QueueReaderService:
    def __init__(self, client: BaseClient, storage: FileStorage):
        self.client = client
        self.storage = storage

    def read_and_save(
        self, queue_name: str, skip: int, take: int, output_file: str
    ) -> int | None:
        try:
            self.client.connect()

            all_messages = self.client.read_messages(queue_name, skip + take)

            if not all_messages:
                return None

            paginated_messages = all_messages[skip : skip + take]

            messages_data = [msg.to_dict() for msg in paginated_messages]

            self.storage.save_json(messages_data, output_file)

            return len(messages_data)

        finally:
            self.client.close()
