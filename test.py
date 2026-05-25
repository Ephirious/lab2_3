import unittest
from main import Task, TaskQueue


class TestTaskQueue(unittest.TestCase):
    """Интеграционные тесты очереди задач: итерация, фильтрация, агрегация."""

    def setUp(self) -> None:
        self.queue = TaskQueue()
        self.queue.add_task(Task("Задача 1", priority=1, status="todo", duration=2))
        self.queue.add_task(Task("Задача 2", priority=3, status="done", duration=3))
        self.queue.add_task(Task("Задача 3", priority=2, status="todo", duration=1))

    def test_iterable_protocol_and_list_conversion(self) -> None:
        tasks_list = list(self.queue)

        self.assertEqual(
            len(tasks_list),
            3,
            msg="Контейнер должен поддерживать полный обход через list()",
        )
        self.assertEqual(
            tasks_list[0].name,
            "Задача 1",
            msg="Порядок элементов при итерации должен совпадать с порядком добавления",
        )

    def test_aggregation_via_sum(self) -> None:
        total_duration = sum(self.queue)

        self.assertEqual(
            total_duration,
            6,
            msg="Встроенная sum() должна корректно агрегировать длительности через __radd__",
        )

    def test_lazy_filter_by_status(self) -> None:
        filtered = list(self.queue.filter_by_status("todo"))

        self.assertEqual(
            len(filtered),
            2,
            msg="Генератор должен отфильтровать задачи по точному совпадению статуса",
        )
        self.assertEqual(filtered[0].name, "Задача 1")
        self.assertEqual(filtered[1].name, "Задача 3")

    def test_lazy_filter_by_priority(self) -> None:
        filtered = list(self.queue.filter_by_priority(2))

        self.assertEqual(
            len(filtered),
            2,
            msg="Фильтр должен оставить задачи с приоритетом >= заданного порога",
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
