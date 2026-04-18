import json
from typing import Iterable
from src.contracts.task import Task

class JsonTaskSource:
    def __init__(self, file_path: str):
        self._file_path = file_path

    def get_tasks(self) -> Iterable[Task]:
        with open(self._file_path, 'r', encoding='utf-8') as f:
            for line in f:
                if not line.strip():
                    continue
                data = json.loads(line)
                yield Task(id=int(data["id"]), payload=data["message"])