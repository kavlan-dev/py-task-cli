import json
import os
import sys
from datetime import datetime

TASKS_FILE = "tasks.json"


class Task:
    def __init__(
        self, id: int, description: str, status: str, created_at: str, updated_at: str
    ):
        self.id = id
        self.description = description
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at


def load_tasks() -> list[Task]:
    """Загрузить задачи из файла JSON"""
    if not os.path.exists(TASKS_FILE):
        return []
    try:
        with open(TASKS_FILE, "r", encoding="utf-8") as f:
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


def save_tasks(tasks: list[Task]) -> None:
    """Сохранить задачи в файл JSON"""
    with open(TASKS_FILE, "w", encoding="utf-8") as f:
        json.dump([task.__dict__ for task in tasks], f, indent=2, ensure_ascii=False)


def generate_id(tasks: list[Task]) -> int:
    """Сгенерировать уникальный ID для новой задачи"""
    if not tasks:
        return 1
    return max(task.id for task in tasks) + 1


def add_task(description: str) -> None:
    """Добавить новую задачу"""
    tasks = load_tasks()
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
    save_tasks(tasks)
    print(f"Task added successfully (ID: {task_id})")


def update_task(task_id: int, new_description: str) -> None:
    """Обновить существующую задачу"""
    tasks = load_tasks()
    for task in tasks:
        if task.id == task_id:
            task.description = new_description
            task.updated_at = datetime.now().isoformat()
            save_tasks(tasks)
            print(f"Task {task_id} updated successfully")
            return
    print(f"Error: Task with ID {task_id} not found")


def delete_task(task_id: int) -> None:
    """Удалить задачу"""
    tasks = load_tasks()
    initial_length = len(tasks)
    tasks = [task for task in tasks if task.id != task_id]

    if len(tasks) < initial_length:
        save_tasks(tasks)
        print(f"Task {task_id} deleted successfully")
    else:
        print(f"Error: Task with ID {task_id} not found")


def mark_task_in_progress(task_id: int) -> None:
    """Отметить задачу как в процессе"""
    tasks = load_tasks()
    for task in tasks:
        if task.id == task_id:
            task.status = "in-progress"
            task.updated_at = datetime.now().isoformat()
            save_tasks(tasks)
            print(f"Task {task_id} marked as in progress")
            return
    print(f"Error: Task with ID {task_id} not found")


def mark_task_done(task_id: int) -> None:
    """Отметить задачу как выполненной"""
    tasks = load_tasks()
    for task in tasks:
        if task.id == task_id:
            task.status = "done"
            task.updated_at = datetime.now().isoformat()
            save_tasks(tasks)
            print(f"Task {task_id} marked as done")
            return
    print(f"Error: Task with ID {task_id} not found")


def list_tasks(status_filter: str | None = None) -> None:
    """Список задач, опционально отфильтрованный по статусу"""
    tasks = load_tasks()

    if status_filter:
        tasks = [task for task in tasks if task.status == status_filter]

    if not tasks:
        print("No tasks found")
        return

    for task in tasks:
        print(f"ID: {task.id}")
        print(f"Description: {task.description}")
        print(f"Status: {task.status}")
        print(f"Created: {task.created_at}")
        print(f"Updated: {task.updated_at}")
        print("-" * 30)


def main():
    if len(sys.argv) < 2:
        print("Использование: task-cli <команда> [аргументы]")
        print("Команды:")
        print("  add <описание> - Добавить новую задачу")
        print("  update <id> <описание> - Обновить задачу")
        print("  delete <id> - Удалить задачу")
        print("  mark-in-progress <id> - Отметить задачу как в процессе")
        print("  mark-done <id> - Отметить задачу как выполненную")
        print(
            "  list [статус] - Показать все задачи (опционально: todo, in-progress, done)"
        )
        return

    cmd = sys.argv[1]
    args = sys.argv[2:]

    if cmd == "add":
        if not args:
            print("Error: Description is required")
            return
        description = " ".join(args)
        add_task(description)

    elif cmd == "update":
        if len(args) < 2:
            print("Error: ID and description are required")
            return
        try:
            task_id = int(args[0])
        except ValueError:
            print("Error: ID must be a number")
            return
        description = " ".join(args[1:])
        update_task(task_id, description)

    elif cmd == "delete":
        if len(args) < 1:
            print("Error: ID is required")
            return
        try:
            task_id = int(args[0])
        except ValueError:
            print("Error: ID must be a number")
            return
        delete_task(task_id)

    elif cmd == "mark-in-progress":
        if len(args) < 1:
            print("Error: ID is required")
            return
        try:
            task_id = int(args[0])
        except ValueError:
            print("Error: ID must be a number")
            return
        mark_task_in_progress(task_id)

    elif cmd == "mark-done":
        if len(args) < 1:
            print("Error: ID is required")
            return
        try:
            task_id = int(args[0])
        except ValueError:
            print("Error: ID must be a number")
            return
        mark_task_done(task_id)

    elif cmd == "list":
        status_filter = None
        if len(args) > 1:
            status_filter = args[1]
            if status_filter not in ["todo", "in-progress", "done"]:
                print("Error: Invalid status filter. Use: todo, in-progress, or done")
                return
        list_tasks(status_filter)

    else:
        print(f"Error: Unknown command '{cmd}'")


if __name__ == "__main__":
    main()
