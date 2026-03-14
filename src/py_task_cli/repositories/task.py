import json
import os

from py_task_cli.models.task import Task
from py_task_cli.repositories.interfaces import ITaskRepository


class TaskRepository(ITaskRepository):
    def __init__(self, tasks_file: str):
        self.tasks_file = tasks_file

    def load_tasks(self) -> list[Task]:
        """Загрузить задачи из файла JSON"""
        if not os.path.exists(self.tasks_file):
            return []
        try:
            with open(self.tasks_file, "r", encoding="utf-8") as f:
                tasks_data = json.load(f)
                return [
                    Task(
                        id=task_data["id"],
                        description=task_data["description"],
                        status=task_data["status"],
                        created_at=task_data["created_at"],
                        updated_at=task_data["updated_at"],
                    )
                    for task_data in tasks_data
                ]
        except Exception:
            return []

    def save_tasks(self, tasks: list[Task]) -> None:
        """Сохранить задачи в файл JSON"""
        with open(self.tasks_file, "w", encoding="utf-8") as f:
            json.dump(
                [task.__dict__ for task in tasks], f, indent=2, ensure_ascii=False
            )
