import json


class FileStorage:
    @staticmethod
    def save_json(data: list[dict], filename: str) -> None:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
