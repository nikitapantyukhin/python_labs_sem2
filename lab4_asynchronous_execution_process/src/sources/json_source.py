import json
from typing import Iterable
from src.contracts.task import Task

class JsonTaskSource:
    def __init__(self, file_path: str):
        self._file_path = file_path

    def get_tasks(self) -> Iterable[Task]:
        try:
            with open(self._file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if not line.strip():
                        continue
                    
                    data = json.loads(line)

                    task = Task(
                        task_id=data.get('id'),
                        description=data.get('description') or data.get('message'),
                        priority=data.get('priority', 50)
                    )

                    if 'status' in data:
                        task.status = data['status']
                    
                    yield task
        
        except FileNotFoundError:
            print(f"Файл {self._file_path} не найден!")