import os
import sys

from main import (
    add_task,
    delete_task,
    list_tasks,
    load_tasks,
    mark_task_done,
    mark_task_in_progress,
    update_task,
)


def test_add_task():
    """Тест добавления новой задачи"""
    print("Тест добавления новой задачи...")
    add_task("Купить молоко")
    tasks = load_tasks()
    task = tasks[0]
    assert len(tasks) == 1
    assert task.description == "Купить молоко"
    assert task.status == "todo"
    print("Тест добавления новой задачи пройден")


def test_update_task():
    """Тест обновления задачи"""
    print("Тест обновления задачи...")
    tasks = load_tasks()
    if tasks:
        task_id = tasks[0].id
        update_task(task_id, "Купить молоко и хлеб")
        tasks = load_tasks()
        updated_task = next((t for t in tasks if t.id == task_id), None)
        assert updated_task is not None
        assert updated_task.description == "Купить молоко и хлеб"
        print("Тест обновления задачи пройден")
    else:
        print("Пропущен тест обновления задачи (нет доступных задач)")


def test_mark_in_progress():
    """Тест отметки задачи как в процессе выполнения"""
    print("Тест отметки задачи как в процессе выполнения...")
    tasks = load_tasks()
    if tasks:
        task_id = tasks[0].id
        mark_task_in_progress(task_id)
        tasks = load_tasks()
        marked_task = next((t for t in tasks if t.id == task_id), None)
        assert marked_task is not None
        assert marked_task.status == "in-progress"
        print("Тест отметки задачи как в процессе выполнения пройден")
    else:
        print(
            "Пропущен тест отметки задачи как в процессе выполнения (нет доступных задач)"
        )


def test_mark_done():
    """Тест отметки задачи как выполненной"""
    print("Тест отметки задачи как выполненной...")
    tasks = load_tasks()
    if tasks:
        task_id = tasks[0].id
        mark_task_done(task_id)
        tasks = load_tasks()
        marked_task = next((t for t in tasks if t.id == task_id), None)
        assert marked_task is not None
        assert marked_task.status == "done"
        print("Тест отметки задачи как выполненной пройден")
    else:
        print("Пропущен тест отметки задачи как выполненной (нет доступных задач)")


def test_list_tasks():
    """Тест вывода списка задач"""
    print("Тест вывода списка задач...")
    print("\nВсе задачи:")
    list_tasks()

    print("\nЗадачи в статусе 'todo':")
    list_tasks("todo")

    print("\nЗадачи в статусе 'in-progress':")
    list_tasks("in-progress")

    print("\nЗадачи в статусе 'done':")
    list_tasks("done")
    print("Тест вывода списка задач пройден")


def test_delete_task():
    """Тест удаления задачи"""
    print("Тест удаления задачи...")
    tasks = load_tasks()
    if tasks:
        task_id = tasks[0].id
        delete_task(task_id)
        tasks = load_tasks()
        assert not any(t.id == task_id for t in tasks)
        print("Тест удаления задачи пройден")
    else:
        print("Пропущен тест удаления задачи (нет доступных задач)")


def cleanup():
    """Очистка тестовых данных"""
    print("\nОчистка тестовых данных...")
    try:
        if os.path.exists("tasks.json"):
            os.remove("tasks.json")
            print("Тестовые данные очищены")
        else:
            print("Нет данных для очистки")
    except Exception as e:
        print(f"Ошибка при очистке: {e}")


def main():
    """Запуск всех тестов"""
    print("Запуск всех тестов...\n")

    try:
        test_add_task()
        test_update_task()
        test_mark_in_progress()
        test_mark_done()
        test_list_tasks()
        test_delete_task()

        print("\n" + "=" * 50)
        print("Все тесты пройдены!")
        print("=" * 50)

    except AssertionError as e:
        print(f"\nТесты не пройдены: {e}")
        sys.exit(1)

    except Exception as e:
        print(f"\nНеожиданная ошибка: {e}")
        sys.exit(1)

    finally:
        cleanup()


if __name__ == "__main__":
    main()
