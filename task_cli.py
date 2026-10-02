import sys
import os
import json
from datetime import datetime

FILE_NAME = "tasks.json"


def load_tasks():
    if not os.path.exists(FILE_NAME):
        return []

    try:
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return []


def save_tasks(tasks):
    with open(FILE_NAME, "w") as file:
        json.dump(tasks, file, indent=2)


def get_current_time():
    return datetime.now().isoformat(timespec="seconds")


def find_task(tasks, task_id):
    for task in tasks:
        if task["id"] == task_id:
            return task

    return None


def add_task(description):
    tasks = load_tasks()

    if tasks:
        new_id = max(task["id"] for task in tasks) + 1
    else:
        new_id = 1

    now = get_current_time()

    task = {
        "id": new_id,
        "description": description,
        "status": "todo",
        "createdAt": now,
        "updatedAt": now
    }

    tasks.append(task)
    save_tasks(tasks)

    print(f"Task added successfully (ID: {new_id})")


def update_task(task_id, description):
    tasks = load_tasks()
    task = find_task(tasks, task_id)

    if task is None:
        print(f"Task with ID {task_id} not found.")
        return

    task["description"] = description
    task["updatedAt"] = get_current_time()

    save_tasks(tasks)

    print(f"Task updated successfully (ID: {task_id})")


def delete_task(task_id):
    tasks = load_tasks()
    task = find_task(tasks, task_id)

    if task is None:
        print(f"Task with ID {task_id} not found.")
        return

    tasks.remove(task)
    save_tasks(tasks)

    print(f"Task deleted successfully (ID: {task_id})")


def mark_task(task_id, status):
    tasks = load_tasks()
    task = find_task(tasks, task_id)

    if task is None:
        print(f"Task with ID {task_id} not found.")
        return

    task["status"] = status
    task["updatedAt"] = get_current_time()

    save_tasks(tasks)

    print(f"Task {task_id} marked as {status}.")


def list_tasks(tasks):
    if not tasks:
        print("No tasks found.")
        return

    for task in tasks:
        print(
            f"{task['id']}. {task['description']} "
            f"[{task['status']}]"
        )


def list_tasks_by_status(status):
    tasks = load_tasks()

    filtered_tasks = [
        task for task in tasks
        if task["status"] == status
    ]

    if not filtered_tasks:
        print(f"No {status} tasks found.")
        return

    list_tasks(filtered_tasks)


def print_usage():
    print("""
Task Tracker CLI

Commands:

  Add a task:
    python task_cli.py add "Buy groceries"

  Update a task:
    python task_cli.py update 1 "Buy groceries and cook dinner"

  Delete a task:
    python task_cli.py delete 1

  Mark task as in-progress:
    python task_cli.py mark-in-progress 1

  Mark task as done:
    python task_cli.py mark-done 1

  List all tasks:
    python task_cli.py list

  List completed tasks:
    python task_cli.py list done

  List todo tasks:
    python task_cli.py list todo

  List in-progress tasks:
    python task_cli.py list in-progress
""")


# Main program

if len(sys.argv) < 2:
    print_usage()
    sys.exit(1)


command = sys.argv[1]


if command == "add":

    if len(sys.argv) < 3:
        print("Please provide a task description.")
        sys.exit(1)

    description = " ".join(sys.argv[2:])
    add_task(description)


elif command == "update":

    if len(sys.argv) < 4:
        print("Usage: python task_cli.py update <id> <description>")
        sys.exit(1)

    try:
        task_id = int(sys.argv[2])
    except ValueError:
        print("Task ID must be a number.")
        sys.exit(1)

    description = " ".join(sys.argv[3:])
    update_task(task_id, description)


elif command == "delete":

    if len(sys.argv) != 3:
        print("Usage: python task_cli.py delete <id>")
        sys.exit(1)

    try:
        task_id = int(sys.argv[2])
    except ValueError:
        print("Task ID must be a number.")
        sys.exit(1)

    delete_task(task_id)


elif command == "mark-in-progress":

    if len(sys.argv) != 3:
        print("Usage: python task_cli.py mark-in-progress <id>")
        sys.exit(1)

    try:
        task_id = int(sys.argv[2])
    except ValueError:
        print("Task ID must be a number.")
        sys.exit(1)

    mark_task(task_id, "in-progress")


elif command == "mark-done":

    if len(sys.argv) != 3:
        print("Usage: python task_cli.py mark-done <id>")
        sys.exit(1)

    try:
        task_id = int(sys.argv[2])
    except ValueError:
        print("Task ID must be a number.")
        sys.exit(1)

    mark_task(task_id, "done")


elif command == "list":

    if len(sys.argv) == 2:
        tasks = load_tasks()
        list_tasks(tasks)

    elif len(sys.argv) == 3:

        status = sys.argv[2]

        if status not in ["done", "todo", "in-progress"]:
            print("Invalid status.")
            print("Use: done, todo, or in-progress.")
            sys.exit(1)

        list_tasks_by_status(status)

    else:
        print("Usage: python task_cli.py list [done|todo|in-progress]")
        sys.exit(1)


else:
    print(f"Unknown command: {command}")
    print_usage()