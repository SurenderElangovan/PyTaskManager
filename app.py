import argparse
import os
from datetime import datetime, timedelta

TASKS_FILE = "tasks.txt"

def load_tasks():
    tasks = []
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r") as file:
            for line in file:
                task_data = line.strip().split(",")
                task = {
                    "name": task_data[0],
                    "due_date": datetime.strptime(task_data[1], "%Y-%m-%d"),
                    "priority": task_data[2],
                    "completed": task_data[3] == "True"
                }
                tasks.append(task)
    return tasks

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as file:
        for task in tasks:
            file.write(f"{task['name']},{task['due_date'].strftime('%Y-%m-%d')},{task['priority']},{task['completed']}\n")

def add_task(name, due_date, priority):
    tasks = load_tasks()
    due_date = datetime.strptime(due_date, "%Y-%m-%d")
    new_task = {"name": name, "due_date": due_date, "priority": priority, "completed": False}
    tasks.append(new_task)
    save_tasks(tasks)
    print(f"Task '{name}' added successfully!")

def list_tasks():
    tasks = load_tasks()
    if tasks:
        print("Task List:")
        for i, task in enumerate(tasks, start=1):
            status = "Completed" if task["completed"] else "Not Completed"
            print(f"{i}. {task['name']} - Due: {task['due_date'].strftime('%Y-%m-%d')}, Priority: {task['priority']}, Status: {status}")
    else:
        print("No tasks found.")

def complete_task(task_index):
    tasks = load_tasks()
    if 1 <= task_index <= len(tasks):
        tasks[task_index - 1]["completed"] = True
        save_tasks(tasks)
        print(f"Task '{tasks[task_index - 1]['name']}' marked as completed.")
    else:
        print("Invalid task index.")

def delete_task(task_index):
    tasks = load_tasks()
    if 1 <= task_index <= len(tasks):
        deleted_task = tasks.pop(task_index - 1)
        save_tasks(tasks)
        print(f"Task '{deleted_task['name']}' deleted successfully.")
    else:
        print("Invalid task index.")

def main():
    parser = argparse.ArgumentParser(description="PyTaskManager - A simple command-line task manager.")
    parser.add_argument("action", choices=["add", "list", "complete", "delete"], help="Action to perform")
    parser.add_argument("--name", help="Task name")
    parser.add_argument("--due", help="Due date (format: YYYY-MM-DD)")
    parser.add_argument("--priority", help="Task priority")
    parser.add_argument("--index", type=int, help="Task index")

    args = parser.parse_args()

    if args.action == "add":
        if not args.name or not args.due or not args.priority:
            print("Error: Please provide task name, due date, and priority.")
        else:
            add_task(args.name, args.due, args.priority)
    elif args.action == "list":
        list_tasks()
    elif args.action == "complete":
        if not args.index:
            print("Error: Please provide the index of the task to complete.")
        else:
            complete_task(args.index)
    elif args.action == "delete":
        if not args.index:
            print("Error: Please provide the index of the task to delete.")
        else:
            delete_task(args.index)

if __name__ == "__main__":
    main()
