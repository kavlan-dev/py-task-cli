from py_task_cli.config import load_config
from py_task_cli.repositories.task import TaskRepository
from py_task_cli.services.task import TaskService

config = load_config()
repository = TaskRepository(config.tasks_file)
service = TaskService(repository)


def get_service() -> TaskService:
    return service
