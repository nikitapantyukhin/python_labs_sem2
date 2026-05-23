import asyncio
import logging

from src.execution.executor import AsyncTaskExecutor
from src.handlers.default import DefaultTaskHandler
from src.handlers.urgent import UrgentTaskHandler
from src.queue.core import TaskQueue
from src.sources.generator_source import GeneratorTaskSource
from src.sources.json_source import JsonTaskSource


async def async_main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(name)s:%(message)s")

    db_file = "tasks.jsonl"

    sources = [
        GeneratorTaskSource(count=3),
        JsonTaskSource(db_file),
    ]

    queue = TaskQueue(sources)
    handlers = [
        UrgentTaskHandler(),
        DefaultTaskHandler(),
    ]

    async with AsyncTaskExecutor(handlers=handlers, worker_count=2) as executor:
        report = await executor.run(queue)

    print(
        "\nГотово: "
        f"загружено={report.loaded}, "
        f"обработано={report.processed}, "
        f"ошибок={report.failed}, "
        f"пропущено={report.skipped}"
    )


def main() -> None:
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
