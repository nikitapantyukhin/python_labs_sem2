import pytest
from src.sources.json_source import JsonTaskSource


def test_json_source_parsing(tmp_path):
    # Создаем временный jsonl файл
    file = tmp_path / "test.jsonl"
    file.write_text('{"id": "10", "message": "hello"}\n{"id": "20", "message": "world"}')

    source = JsonTaskSource(str(file))
    tasks = list(source.get_tasks())

    assert len(tasks) == 2
    assert tasks[0].id == 10
    assert tasks[1].payload == "world"