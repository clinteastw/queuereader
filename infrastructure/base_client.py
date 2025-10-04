from abc import ABC, abstractmethod
from typing import Any


class BaseClient(ABC):
    @abstractmethod
    def connect(self) -> None:
        pass

    @abstractmethod
    def read_messages(self, queue_name: str, count: int) -> list[dict[str, Any]]:
        pass

    @abstractmethod
    def close(self) -> None:
        pass
