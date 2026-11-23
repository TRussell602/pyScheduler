
class Task:
    def __init__(self, name, desc):
        self.name = name
        self.desc = desc


class Course:
    def __init__(self, code, name):
        self.code = code
        self.name = name
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)


# ========== BASIC TEST ============
#
#comp2633 = Course("COMP2633", "Software Engineering")
#
#taskA = Task("Sprint 1", "Complete the Tutorial Doc")
#
#comp2633.add_task(taskA)
#
#for task in comp2633.tasks:
#    print(task.name)