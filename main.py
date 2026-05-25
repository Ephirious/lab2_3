from __future__ import annotations
from typing import Generator, Any
from dataclasses import dataclass


@dataclass
class Task:
    """Модель отдельной задачи."""

    name: str
    priority: int
    status: str
    duration: int

    def __radd__(self, other: Any) -> int:
        """Обратное сложение для корректной работы встроенной sum()."""
        if isinstance(other, int):
            return other + self.duration
        return self.duration


class TaskIterator:
    """Итератор очереди задач. Обеспечивает пошаговый обход коллекции."""

    def __init__(self, tasks: list[Task]) -> None:
        self._tasks = tasks
        self._index = 0

    def __iter__(self) -> TaskIterator:
        return self

    def __next__(self) -> Task:
        if self._index >= len(self._tasks):
            raise StopIteration

        task = self._tasks[self._index]
        self._index += 1
        return task


class TaskQueue:
    """Итерируемый контейнер для хранения и фильтрации задач."""

    def __init__(self) -> None:
        self._tasks: list[Task] = []

    def __iter__(self) -> TaskIterator:
        return TaskIterator(self._tasks)

    def add_task(self, task: Task) -> None:
        self._tasks.append(task)

    def filter_by_status(self, target_status: str) -> Generator[Task, None, None]:
        """Ленивая фильтрация задач по статусу."""
        for task in self._tasks:
            if task.status == target_status:
                yield task

    def filter_by_priority(self, min_priority: int) -> Generator[Task, None, None]:
        """Ленивая фильтрация задач по минимальному приоритету."""
        for task in self._tasks:
            if task.priority >= min_priority:
                yield task


if __name__ == "__main__":
    queue = TaskQueue()
    queue.add_task(Task("Написать код", priority=2, status="done", duration=3))
    queue.add_task(Task("Проверить баги", priority=1, status="todo", duration=2))
    queue.add_task(Task("Открыть пулл-реквест", priority=3, status="todo", duration=1))

    print("1. Повторный обход очереди циклом for:")
    for task in queue:
        print(f" - {task.name}")
    for task in queue:
        pass

    print("\n2. Совместимость с функцией list():")
    tasks_list = list(queue)
    print(f" Количество задач в списке: {len(tasks_list)}")

    print("\n3. Работа ленивого генератора (фильтр по статусу 'todo'):")
    for task in queue.filter_by_status("todo"):
        print(f" - {task.name}")

    print("\n4. Совместимость со стандартной функцией sum():")
    total_time = sum(queue)
    print(f" Итоговое время выполнения всех задач: {total_time} ч.")
