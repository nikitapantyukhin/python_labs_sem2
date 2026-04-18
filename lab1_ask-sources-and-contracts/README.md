# Лабораторная работа №1: Источники задач и контракты

### Описание проекта
Проект представляет собой систему сбора задач из различных источников (JSON-файлы, генераторы), объединенных единым интерфейсом.

**Основные возможности:**
* Хранение задач с полями `id` и `payload`.
* Единый контракт для всех источников через `typing.Protocol`.
* Автоматическая генерация данных и чтение из `.jsonl` (JSON Lines).
* Валидация источников в рантайме с помощью `@runtime_checkable`.
* Покрытие кода тестами >90%.

### Что было изучено
* **Duck Typing:** реализация гибкого взаимодействия объектов без жесткого наследования.
* **Protocols:** описание поведенческих контрактов (PEP 544).
* **Runtime Checks:** использование `isinstance()` для проверки соответствия протоколу в процессе выполнения.
* **Package Structure:** организация проекта с разделением на контракты (`contracts`), источники (`sources`) и ядро (`inbox`).

### Структура проекта
```text
├─ .pre-commit-config.yaml
├─ pyproject.toml
├─ README.md
├── src/
│   ├── __init__.py
│   ├── main.py              # Точка входа в программу
│   ├── contracts/
│   │   ├── source.py        # Протокол TaskSource
│   │   └── task.py          # Dataclass Task
│   ├── inbox/
│   │   └── core.py          # Логика сбора задач (TaskInbox)
│   └── sources/
│       ├── generator_source.py
│       └── json_source.py
├── tests/                   # Набор unit-тестов
├── tasks.jsonl              
├── pyproject.toml           
├── requirements.txt         
└── Dockerfile               
└── uv.lock
```

### Установка и запуск

**Локальная установка зависимостей:**
```bash
pip install -r requirements.txt
```

**Запуск основной программы:**
```bash
python -m src.main
```

**Запуск тестов и проверка покрытия:**
```bash
pytest --cov=src tests/
```

### Работа в Docker


**1. Сборка образа:**
```bash
docker build -t lab1-tasks .
```

**2. Запуск тестов и отчета о покрытии (по умолчанию):**
```bash
docker run --rm lab1-tasks
```

**3. Запуск самой программы внутри контейнера:**
```bash
docker run --rm lab1-tasks python -m src.main
```
