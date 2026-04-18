import pytest
from src.inbox.core import TaskInbox
from src.sources.generator_source import GeneratorTaskSource


def test_inbox_iteration_logic():
    sources = [GeneratorTaskSource(count=2), GeneratorTaskSource(count=3)]
    inbox = TaskInbox(sources)

    tasks = list(inbox.iter_tasks())
    assert len(tasks) == 5


def test_inbox_raises_type_error_on_invalid_source():
    inbox = TaskInbox(["Not a real source"])
    with pytest.raises(TypeError) as excinfo:
        list(inbox.iter_tasks())
    assert "does not implement TaskSource protocol" in str(excinfo.value)