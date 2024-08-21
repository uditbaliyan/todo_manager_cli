import mysql.connector
from typing import List
import datetime
from model import Todo

# Establish the connection to the MySQL database
conn = mysql.connector.connect(
    host="localhost",
    user="your_username",
    password="your_password",
    database="your_database"
)
c = conn.cursor()

# Function to create the todos table if it doesn't exist
def create_table():
    c.execute("""
        CREATE TABLE IF NOT EXISTS todos (
            task VARCHAR(255) NOT NULL,
            category VARCHAR(255),
            date_added DATETIME NOT NULL,
            date_completed DATETIME,
            status INT NOT NULL CHECK (status IN (0, 1, 2)),
            position INT UNIQUE NOT NULL
        )
    """)

create_table()

# Function to insert a new todo into the database
def insert_todo(todo: Todo):
    try:
        c.execute('SELECT COUNT(*) FROM todos')
        count = c.fetchone()[0]
        todo.position = count if count else 0
        
        with conn:
            c.execute('''
                INSERT INTO todos (task, category, date_added, date_completed, status, position) 
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', (
                todo.task, 
                todo.category, 
                todo.date_added,
                todo.date_completed, 
                todo.status, 
                todo.position 
            ))
    except mysql.connector.Error as e:
        print(f"An error occurred: {e}")

# Function to retrieve all todos from the database
def get_all_todos() -> List[Todo]:
    try:
        c.execute('SELECT * FROM todos ORDER BY position')
        results = c.fetchall()
        return [Todo(*result) for result in results]
    except mysql.connector.Error as e:
        print(f"An error occurred: {e}")
        return []

# Function to delete a todo based on its position
def delete_todo(position: int):
    try:
        c.execute('SELECT COUNT(*) FROM todos')
        count = c.fetchone()[0]

        with conn:
            c.execute("DELETE FROM todos WHERE position = %s", (position,))
            for pos in range(position + 1, count):
                change_position(pos, pos - 1, False)
            conn.commit()
    except mysql.connector.Error as e:
        print(f"An error occurred: {e}")

# Function to change the position of a todo in the list
def change_position(old_position: int, new_position: int, commit=True):
    try:
        c.execute('UPDATE todos SET position = %s WHERE position = %s', (new_position, old_position))
        if commit:
            conn.commit()
    except mysql.connector.Error as e:
        print(f"An error occurred: {e}")

# Function to update the task and/or category of a todo
def update_todo(position: int, task: str = None, category: str = None):
    try:
        with conn:
            if task and category:
                c.execute('UPDATE todos SET task = %s, category = %s WHERE position = %s', (task, category, position))
            elif task:
                c.execute('UPDATE todos SET task = %s WHERE position = %s', (task, position))
            elif category:
                c.execute('UPDATE todos SET category = %s WHERE position = %s', (category, position))
    except mysql.connector.Error as e:
        print(f"An error occurred: {e}")

# Function to mark a todo as completed
def complete_todo(position: int):
    try:
        with conn:
            c.execute('''
                UPDATE todos 
                SET status = 2, date_completed = %s 
                WHERE position = %s
            ''', (datetime.datetime.now().isoformat(), position))
    except mysql.connector.Error as e:
        print(f"An error occurred: {e}")


# ------------------------------------------------------------------------------------------


# import sqlite3
# from typing import List
# import datetime
# from model import Todo

# # Establish the connection to the database
# conn = sqlite3.connect('todos.db')
# c = conn.cursor()

# # Function to create the todos table if it doesn't exist
# def create_table():
#     c.execute("""
#         CREATE TABLE IF NOT EXISTS todos (
#             task TEXT NOT NULL,
#             category TEXT,
#             date_added TEXT NOT NULL,
#             date_completed TEXT,
#             status INTEGER NOT NULL CHECK(status IN (0, 1, 2)),
#             position INTEGER UNIQUE NOT NULL
#         )
#     """)

# create_table()

# # Function to insert a new todo into the database
# def insert_todo(todo: Todo):
#     try:
#         c.execute('SELECT COUNT(*) FROM todos')
#         count = c.fetchone()[0]
#         todo.position = count if count else 0
        
#         with conn:
#             c.execute('''
#                 INSERT INTO todos (task, category, date_added, date_completed, status, position) 
#                 VALUES (:task, :category, :date_added, :date_completed, :status, :position)
#             ''', {
#                 'task': todo.task, 
#                 'category': todo.category, 
#                 'date_added': todo.date_added,
#                 'date_completed': todo.date_completed, 
#                 'status': todo.status, 
#                 'position': todo.position 
#             })
#     except sqlite3.Error as e:
#         print(f"An error occurred: {e}")

# # Function to retrieve all todos from the database
# def get_all_todos() -> List[Todo]:
#     try:
#         c.execute('SELECT * FROM todos ORDER BY position')
#         results = c.fetchall()
#         return [Todo(*result) for result in results]
#     except sqlite3.Error as e:
#         print(f"An error occurred: {e}")
#         return []

# # Function to delete a todo based on its position
# def delete_todo(position: int):
#     try:
#         c.execute('SELECT COUNT(*) FROM todos')
#         count = c.fetchone()[0]

#         with conn:
#             c.execute("DELETE FROM todos WHERE position = :position", {"position": position})
#             for pos in range(position + 1, count):
#                 change_position(pos, pos - 1, False)
#             conn.commit()
#     except sqlite3.Error as e:
#         print(f"An error occurred: {e}")

# # Function to change the position of a todo in the list
# def change_position(old_position: int, new_position: int, commit=True):
#     try:
#         c.execute('UPDATE todos SET position = :position_new WHERE position = :position_old', {
#             'position_old': old_position, 
#             'position_new': new_position
#         })
#         if commit:
#             conn.commit()
#     except sqlite3.Error as e:
#         print(f"An error occurred: {e}")

# # Function to update the task and/or category of a todo
# def update_todo(position: int, task: str = None, category: str = None):
#     try:
#         with conn:
#             if task and category:
#                 c.execute('UPDATE todos SET task = :task, category = :category WHERE position = :position', {
#                     'position': position, 'task': task, 'category': category
#                 })
#             elif task:
#                 c.execute('UPDATE todos SET task = :task WHERE position = :position', {
#                     'position': position, 'task': task
#                 })
#             elif category:
#                 c.execute('UPDATE todos SET category = :category WHERE position = :position', {
#                     'position': position, 'category': category
#                 })
#     except sqlite3.Error as e:
#         print(f"An error occurred: {e}")

# # Function to mark a todo as completed
# def complete_todo(position: int):
#     try:
#         with conn:
#             c.execute('''
#                 UPDATE todos 
#                 SET status = 2, date_completed = :date_completed 
#                 WHERE position = :position
#             ''', {
#                 'position': position, 
#                 'date_completed': datetime.datetime.now().isoformat()
#             })
#     except sqlite3.Error as e:
#         print(f"An error occurred: {e}")
