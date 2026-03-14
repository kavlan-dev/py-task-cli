from py_task_cli.models.task import Task


def generate_id(tasks: list[Task]) -> int:
    """Сгенерировать уникальный ID для новой задачи"""
    if not tasks:
        return 1
    return max(task.id for task in tasks) + 1
