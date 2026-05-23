# Лабораторная работа №4: Асинхронный исполнитель задач

### Описание проекта

Проект расширяет лабораторную работу №3. Синхронные источники задач и ленивая `TaskQueue` сохранены, а поверх них добавлен асинхронный слой обработки задач.

Теперь система умеет:

* загружать задачи из синхронной очереди в `asyncio.Queue`;
* обрабатывать задачи несколькими асинхронными воркерами;
* выбирать обработчик через контракт `TaskHandler`;
* управлять жизненным циклом исполнителя через `async with`;
* централизованно логировать успешную обработку и ошибки;
* продолжать работу, если отдельная задача завершилась с ошибкой.


### Что было добавлено

* **Асинхронная очередь:** `AsyncTaskQueue` на основе `asyncio.Queue`.
* **Контракт обработчика:** `TaskHandler` через `typing.Protocol` и `@runtime_checkable`.
* **Асинхронный исполнитель:** `AsyncTaskExecutor` запускает воркеры и распределяет задачи по обработчикам.
* **Контекстный менеджер:** исполнитель поддерживает `__aenter__` и `__aexit__`.
* **Обработка ошибок:** сбои обработчиков фиксируются в отчете, а задача получает статус `Failed`.
* **Примерные обработчики:** `UrgentTaskHandler` для срочных задач и `DefaultTaskHandler` для остальных.

### Структура проекта

```
├── THEORY_LAB4.md
├── README.md
├── pyproject.toml
├── requirements.txt
├── Dockerfile
├── tasks.jsonl
├── src/
│   ├── main.py
│   ├── contracts/
│   │   ├── handler.py
│   │   ├── source.py
│   │   └── task.py
│   ├── execution/
│   │   ├── async_queue.py
│   │   └── executor.py
│   ├── handlers/
│   │   ├── default.py
│   │   └── urgent.py
│   ├── queue/
│   │   └── core.py
│   └── sources/
│       ├── generator_source.py
│       └── json_source.py
└── tests/
```

### Установка и запуск

**Локальная установка зависимостей:**

```bash
pip install -r requirements.txt
```

**Запуск основной программы:**

```bash
python3 -m src.main
```

**Запуск тестов и проверка покрытия:**

```bash
pytest --cov=src tests/
```

### Работа в Docker

**Сборка образа:**

```bash
docker build -t lab4-async-tasks .
```

**Запуск тестов внутри контейнера:**

```bash
docker run --rm lab4-async-tasks
```

**Запуск демонстрации асинхронного исполнителя:**

```bash
docker run --rm lab4-async-tasks python -m src.main
```
