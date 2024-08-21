from model import Todo
from database import get_all_todos, delete_todo, insert_todo, complete_todo, update_todo

def add(task: str, category: str):
    print(f"Adding: Task='{task}', Category='{category}'")
    todo = Todo(task, category)
    insert_todo(todo)
    show()

def delete(position: int):
    print(f"Deleting task at position: {position}")
    delete_todo(position - 1)
    show()

def update(position: int, task: str = None, category: str = None):
    print(f"Updating task at position: {position}")
    update_todo(position - 1, task, category)
    show()

def complete(position: int):
    print(f"Completing task at position: {position}")
    complete_todo(position - 1)
    show()

def show():
    tasks = get_all_todos()
    print("\nTodos:")
    print("{:<6} {:<20} {:<12} {:<6}".format("No.", "Todo", "Category", "Done"))
    print("-" * 46)

    def get_category_color(category):
        COLORS = {'Learn': 'cyan', 'YouTube': 'red', 'Sports': 'cyan', 'Study': 'green'}
        return COLORS.get(category, 'white')

    for idx, task in enumerate(tasks, start=1):
        is_done_str = '✅' if task.status == 2 else '❌'
        print("{:<6} {:<20} {:<12} {:<6}".format(idx, task.task, task.category, is_done_str))
    print("-" * 46)

def main():
    while True:
        print("\nOptions: add, delete, update, complete, show, exit")
        command = input("Enter command: ").strip().lower()
        
        if command == "add":
            task = input("Enter task: ")
            category = input("Enter category: ")
            add(task, category)
        elif command == "delete":
            position = int(input("Enter position: "))
            delete(position)
        elif command == "update":
            position = int(input("Enter position: "))
            task = input("Enter new task (or leave blank to keep current): ").strip() or None
            category = input("Enter new category (or leave blank to keep current): ").strip() or None
            update(position, task, category)
        elif command == "complete":
            position = int(input("Enter position: "))
            complete(position)
        elif command == "show":
            show()
        elif command == "exit":
            break
        else:
            print("Unknown command. Please try again.")

if __name__ == "__main__":
    main()
