import sys

from py_task_cli.depends import get_service


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

    service = get_service()

    if cmd == "add":
        if not args:
            print("Error: Description is required")
            return
        description = " ".join(args)
        task = service.add_task(description)
        print(f"Task added successfully (ID: {task.id})")

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
        if service.update_task(task_id, description):
            print(f"Task updated successfully (ID: {task_id})")
        else:
            print(f"Error: Task with ID {task_id} not found")

    elif cmd == "delete":
        if len(args) < 1:
            print("Error: ID is required")
            return
        try:
            task_id = int(args[0])
        except ValueError:
            print("Error: ID must be a number")
            return
        if service.delete_task(task_id):
            print(f"Task deleted successfully (ID: {task_id})")
        else:
            print(f"Error: Task with ID {task_id} not found")

    elif cmd == "mark-in-progress":
        if len(args) < 1:
            print("Error: ID is required")
            return
        try:
            task_id = int(args[0])
        except ValueError:
            print("Error: ID must be a number")
            return
        if service.mark_task(task_id, "in-progress"):
            print(f"Task marked as in-progress (ID: {task_id})")
        else:
            print(f"Error: Task with ID {task_id} not found")

    elif cmd == "mark-done":
        if len(args) < 1:
            print("Error: ID is required")
            return
        try:
            task_id = int(args[0])
        except ValueError:
            print("Error: ID must be a number")
            return
        if service.mark_task(task_id, "done"):
            print(f"Task marked as done (ID: {task_id})")
        else:
            print(f"Error: Task with ID {task_id} not found")

    elif cmd == "list":
        status_filter = None
        if len(args) > 1:
            status_filter = args[1]
            if status_filter not in ["todo", "in-progress", "done"]:
                print("Error: Invalid status filter. Use: todo, in-progress, or done")
                return
        tasks = service.list_tasks(status_filter)
        if len(tasks) == 0:
            print("No tasks found")
            return
        for task in tasks:
            print(f"ID: {task.id}")
            print(f"Description: {task.description}")
            print(f"Status: {task.status}")
            print(f"Created: {task.created_at}")
            print(f"Updated: {task.updated_at}")
            print("-" * 30)

    else:
        print(f"Error: Unknown command '{cmd}'")


if __name__ == "__main__":
    main()
