
class Task:
    def __init__(self, name, desc):
        self.name = name
        self.desc = desc
        self.prev = None
        self.next = None

class Course:
    def __init__(self, code, name):
        self.code = code
        self.name = name
        self.head = None
        self.tail = None

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

        

