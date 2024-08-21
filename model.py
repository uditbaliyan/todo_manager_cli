import datetime

class Todo:
    def __init__(self, task: str, category: str = None, 
                 date_added: str = None, date_completed: str = None,
                 status: int = None, position: int = None):
        self.task = task
        self.category = category
        self.date_added = date_added if date_added is not None else datetime.datetime.now().isoformat()
        self.date_completed = date_completed
        self.status = status if status is not None else 1  # 1 = open, 2 = completed
        self.position = position

    def __repr__(self) -> str:
        return f"Todo(task={self.task!r}, category={self.category!r}, date_added={self.date_added!r}, " \
               f"date_completed={self.date_completed!r}, status={self.status!r}, position={self.position!r})"
