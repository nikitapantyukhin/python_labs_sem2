import os
from src.inbox.core import TaskInbox
from src.sources.generator_source import GeneratorTaskSource
from src.sources.json_source import JsonTaskSource

def main():
    db_file = "tasks.jsonl"

    if not os.path.exists(db_file):
        with open(db_file, "w", encoding="utf-8") as f:
            f.write('{"id": 1, "message": "First task from file"}\n')
            f.write('{"id": 2, "message": "Second task from file"}\n')
        print(f"Created initial {db_file}")

    sources = [
        GeneratorTaskSource(count=2),
        JsonTaskSource(db_file)
    ]

    inbox = TaskInbox(sources)

    for task in inbox.iter_tasks():
        print(f"ID: {task.id} | Payload: {task.payload}")

if __name__ == "__main__":
    main()