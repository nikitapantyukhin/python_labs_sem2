from datetime import datetime


class IntegerRange:
    """Дескриптор для проверки целых чисел в диапазоне"""
    def __init__(self, min_val = None, max_val = None):
        self.min_val = min_val
        self.max_val = max_val
        self.name = None
    
    def __set_name__(self, owner, name):
        self.name = f"_{name}"
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self.name)

    def __set__(self, instance, value):
        if not isinstance(value, int):
            raise TypeError(f"{self.name} должен быть целым числом!")
        
        if (self.min_val is not None and value < self.min_val) or \
            (self.max_val is not None and value > self.max_val):
            raise ValueError(f"Значение {value} вне диапазона [{self.min_val}, {self.max_val}]")

        setattr(instance, self.name, value)


class Choice:
    """Дескриптор для проверки, что статус входит в список существующих"""
    def __init__(self, *options):
        self.options = options
        self.name = None
    
    def __set_name__(self, owner, name):
        self.name = f"_{name}"
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self.name)
    
    def __set__(self, instance, value):
        if value not in self.options:
            raise ValueError(f"Недопустимое значение {value}. Есть только {self.options}")
        
        setattr(instance, self.name, value)


class Task:
    priority = IntegerRange(min_val = 0, max_val = 100)
    status = Choice("New", "In Progress", "Done")

    def __init__(self, task_id: int, description: str, priority: int):
        self._id = task_id
        self._created = datetime.now()
        self.description = description
        self.priority = priority
        self.status = "New"
    
    @property
    def id(self):
        return self._id
    
    @property
    def created(self):
        return self._created

    @property
    def is_urgent(self):
        return self.priority > 80
    
    def __repr__(self):
        return f"Task: id: {self.id}, status: {self.status}, priority: {self.priority}"
