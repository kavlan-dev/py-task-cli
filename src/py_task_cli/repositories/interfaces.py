from abc import ABC, abstractmethod


class ITaskRepository(ABC):
    @abstractmethod
    def load_tasks(self) -> list:
        pass

    @abstractmethod
    def save_tasks(self, tasks: list) -> None:
        pass
