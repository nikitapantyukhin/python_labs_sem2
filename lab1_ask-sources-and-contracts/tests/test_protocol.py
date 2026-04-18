from src.contracts.source import TaskSource
from src.sources.generator_source import GeneratorTaskSource


def test_task_source_protocol_compliance():
    # GeneratorTaskSource должен соответствовать протоколу TaskSource
    source = GeneratorTaskSource(count=1)
    assert isinstance(source, TaskSource)


def test_invalid_source_compliance():
    class NotASource:
        pass

    bad_source = NotASource()
    assert not isinstance(bad_source, TaskSource)