from src.contracts.task import Task

def test_task_creation():
    task = Task(id=1, payload="test data")
    assert task.id == 1
    assert task.payload == "test data"

def test_task_immutability():
    import pytest
    task = Task(id=1, payload="test")
    with pytest.raises(AttributeError):
        task.id = 2  # dataclass(frozen=True)