
class Task:
    def __init__(self, name, desc, start_time, end_time, do_by):
        self.name = name
        self.desc = desc
        self.start_time = start_time
        self.end_time = end_time
        self.do_by = do_by
        self.prev = None
        self.next = None

class Course:
    def __init__(self, code, name):
        self.code = code
        self.name = name
        self.head = None
        self.tail = None
        self.prev = None
        self.next = None

    def add_task(self, task):

        # If the list is empty
        if self.head == None:
            self.head = task
            self.tail = task

        else:
            # Connect the new task to the end
            self.tail.next = task
            task.prev = self.tail

            # Update the tail
            self.tail = task

    def find_task(self, name):

        curr = self.head

        while curr != None:

            if curr.name == name:
                return curr

            curr = curr.next

        return None

    def remove_task(self, name):

        curr = self.head

        while curr != None:

            if curr.name == name:

                # Update previous node
                if curr.prev != None:
                    curr.prev.next = curr.next
                else:
                    self.head = curr.next

                # Update next node
                if curr.next != None:
                    curr.next.prev = curr.prev
                else:
                    self.tail = curr.prev

                curr.prev = None
                curr.next = None

                return True

            curr = curr.next

        return False

class Courselist:
    def __init__(self):
        self.head = None
        self.tail = None

    def add_task(self, course):

        # If the list is empty
        if self.head == None:
            self.head = course
            self.tail = course

        else:
            # Connect the new task to the end
            self.tail.next = course
            course.prev = self.tail

            # Update the tail
            self.tail = course     

