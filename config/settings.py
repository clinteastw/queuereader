import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class Settings:
    kafka_bootstrap_servers: str
    rabbitmq_host: str
    rabbitmq_port: int
    rabbitmq_user: str
    rabbitmq_password: str

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            kafka_bootstrap_servers=os.getenv(
                "KAFKA_BOOTSTRAP_SERVERS",
            ),
            rabbitmq_host=os.getenv("RABBITMQ_HOST"),
            rabbitmq_port=int(os.getenv("RABBITMQ_PORT")),
            rabbitmq_user=os.getenv("RABBITMQ_USER"),
            rabbitmq_password=os.getenv("RABBITMQ_PASSWORD"),
        )


settings: Optional[Settings] = None


def get_settings() -> Settings:
    global settings
    if settings is None:
        settings = Settings.from_env()
    return settings
