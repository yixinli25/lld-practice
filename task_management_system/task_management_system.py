from enum import Enum
from collections import defaultdict

# 1. The task management system should allow users to create, update, and delete tasks.
# 2. Each task should have a title, description, due date, priority, and status (e.g., pending, in progress, completed).
# 3. Users should be able to assign tasks to other users and set reminders for tasks.
# 4. The system should support searching and filtering tasks based on various criteria (e.g., priority, due date, assigned user).
# 5. Users should be able to mark tasks as completed and view their task history.
# 6. The system should handle concurrent access to tasks and ensure data consistency.
# 7. The system should be extensible to accommodate future enhancements and new features.

class User:
    def __init__(self, user_id: int, user_name: str, email: str):
        self.user_id = user_id
        self.user_name = user_name
        self.email = email

    def get_user_id(self):
        return self.user_id
    
    def get_user_name(self):
        return self.user_name
    
    def get_user_email(self):
        return self.email
    

class TaskStatus(Enum):
    PENDING = 1
    IN_PROGRESS = 2
    COMPLETED = 3


class Task:
    def __init__(
            self, 
            task_id: int, 
            title: str, 
            description: str, 
            due_date: str, 
            priority: str, 
            assigned_by: User,
            assgined_to: User
        ):
        self.id = task_id
        self.title = title
        self.description = description
        self.due_date = due_date
        self.priority = priority
        self.status = TaskStatus.PENDING.name
        self.assigned_by = assigned_by
        self.assigned_to = assgined_to

    def get_id(self):
        return self.id
    
    def get_title(self):
        return self.title
    
    def get_description(self):
        return self.description
    
    def get_due_date(self):
        return self.due_date
    
    def get_priority(self):
        return self.priority
    
    def get_status(self):
        return self.status
    
    def get_assigned_to_user(self):
        return self.assigned_to
    
    def get_assigned_by_user(self):
        return self.assigned_by
    
    def set_title(self, title: str):
        self.title = title

    def set_description(self, description: str):
        self.description = description

    def set_due_date(self, due_date: str):
        self.due_date = due_date

    def set_priority(self, priority: str):
        self.priority = priority

    def set_status(self, status: str):
        self.status = status


class TaskManager:
    _instance = None

    def __init__(self):
        if TaskManager._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            TaskManager._instance = self
            self.tasks = {}
            self.user_tasks = defaultdict(list)

    @staticmethod
    def get_instance():
        if TaskManager._instance is None:
            TaskManager()

        return TaskManager._instance
    
    def create_task(self, task: Task):
        self.tasks[task.get_id()] = task
        self._assign_task_to_user(task.get_assigned_to_user(), task)
        
    def update_task(self, updated_task: Task):
        if updated_task.get_id() in self.tasks:
            existing_task = self.tasks[updated_task.get_id()]
            existing_task.set_title(updated_task.get_title())
            existing_task.set_description(updated_task.get_description())
            existing_task.set_due_date(updated_task.get_due_date())
            existing_task.set_priority(updated_task.get_priority())
            existing_task.set_status(updated_task.get_status())
            existing_task.set_title(updated_task.get_title())
            
            previous_assigned_to = existing_task.get_assigned_to_user()
            updated_assigned_to = updated_task.get_assigned_to_user()

            if previous_assigned_to != updated_assigned_to:
                self._unassign_task_from_user(previous_assigned_to, existing_task)
                self._assign_task_to_user(updated_assigned_to, existing_task)

    def delete_task(self, task_id):
        if task_id in self.tasks:
            task = self.tasks[task_id]
            self._unassign_task_from_user(task.get_assigned_to_user(), task)
            del self.tasks[task_id]

    def search_tasks(self, keyword):
        matching_tasks = []
        for task in self.tasks.values():
            if (
                keyword in task.get_title() 
                or keyword in task.get_description()
                or keyword in task.get_priority()
                or keyword in task.get_assigned_to_user().get_user_name()
            ):
                matching_tasks.append(task)

        return matching_tasks
    
    def filter_tasks(self, status, start_date, end_date, priority):
        filtered_tasks = []
        for task in self.tasks.values():
            if (
                task.get_status() == status
                and start_date <= task.get_due_date() <= end_date
                and task.get_priority() == priority
            ):
                filtered_tasks.append(task)

        return filtered_tasks
    
    def mark_task_as_completed(self, task_id):
        if task_id in self.tasks:
            task = self.tasks[task_id]
            task.set_status(TaskStatus.COMPLETED)

    def get_task_history(self, user):
        return self.user_tasks[user.get_user_id()]

    def _assign_task_to_user(self, assigned_to: User, task: Task):
        self.user_tasks[assigned_to].append(task)

    def _unassign_task_from_user(self, user: User, task: Task):
        if task not in self.user_tasks[user]:
            raise Exception(f"Task was not assigned to user {user.get_user_name()}")
        
        for i, t in enumerate(self.user_tasks[user]):
            if t == task:
                self.user_tasks[user].pop(i)