from dataclasses import dataclass
from typing import Any


@dataclass
class Message:
    id: int
    body: str
    metrics: dict[str, int] | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Message":
        return cls(
            id=data.get("Id", 0), body=data.get("Body", ""), metrics=data.get("Metrics")
        )

    def to_dict(self) -> dict[str, Any]:
        result = {"Id": self.id, "Body": self.body}
        if self.metrics:
            result["Metrics"] = self.metrics
        return result
