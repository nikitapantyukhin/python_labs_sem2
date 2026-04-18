from src.sources.generator_source import GeneratorTaskSource
from src.contracts.task import Task


def test_generator_emits_correct_number_of_tasks():
    count = 5
    source = GeneratorTaskSource(count=count)
    tasks = list(source.get_tasks())

    assert len(tasks) == count
    assert all(isinstance(t, Task) for t in tasks)
    assert tasks[0].id == 1