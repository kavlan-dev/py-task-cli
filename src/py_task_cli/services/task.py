from datetime import datetime
from typing import List, Optional

from py_task_cli.models.task import Task
from py_task_cli.repositories.interfaces import ITaskRepository
from py_task_cli.utils.util import generate_id


class TaskService:
    def __init__(self, repository: ITaskRepository):
        self.repository = repository

    def add_task(self, description: str) -> Task:
        """Добавить новую задачу"""
        tasks = self.repository.load_tasks()
        task_id = generate_id(tasks)
        now = datetime.now().isoformat()

        new_task = Task(
            id=task_id,
            description=description,
            status="todo",
            created_at=now,
            updated_at=now,
        )

        tasks.append(new_task)
        self.repository.save_tasks(tasks)
        return new_task

    def update_task(self, task_id: int, new_description: str) -> Optional[Task]:
        """Обновить существующую задачу"""
        tasks = self.repository.load_tasks()
        for task in tasks:
            if task.id == task_id:
                task.description = new_description
                task.updated_at = datetime.now().isoformat()
                self.repository.save_tasks(tasks)
                return task
        return

    def delete_task(self, task_id: int) -> bool:
        """Удалить задачу"""
        tasks = self.repository.load_tasks()
        initial_length = len(tasks)
        tasks = [task for task in tasks if task.id != task_id]

        if len(tasks) < initial_length:
            self.repository.save_tasks(tasks)
            return True
        else:
            return False

    def mark_task(self, task_id: int, status: str) -> Optional[Task]:
        """Отметить задачу"""
        if status not in ["in-progress", "done"]:
            return

        tasks = self.repository.load_tasks()
        for task in tasks:
            if task.id == task_id:
                task.status = status
                task.updated_at = datetime.now().isoformat()
                self.repository.save_tasks(tasks)
                return task
        return

    def list_tasks(self, status_filter: Optional[str] = None) -> List[Task]:
        """Список задач, опционально отфильтрованный по статусу"""
        tasks = self.repository.load_tasks()

        if status_filter:
            tasks = [task for task in tasks if task.status == status_filter]

        return tasks
