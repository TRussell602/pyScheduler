from pathlib import Path
from objects import Course, Task, Courselist


# the SaveData file holds data in the following form.
# Code/ Name/ name, description, start_time, end_time, do_by + name, description, start_time, end_time, do_by&
# Code/ Name/ name, description, start_time, end_time, do_by + name, description, start_time, end_time, do_by

class SaveFile:
    # used to construct the class so load and save are accessible.
    def __init__(self):
        # create a file to hold information about the cources and 
        self.file = Path('../SaveData.txt')

    # used to save the data about Courses and their tasks every time one of them is updated.
    # takes a list of course as input nad returns null.
    def save(self, course_list: Courselist): # we may need an object that holds multiple courses
        # opens the save_file in order to write data into it.
        with open(self.file, 'w') as save_file:
            temp = course_list
            # full loop for writeing the information for each course and its tasks into the file.
            while temp.head != None:
                # writes the code and name of the current course
                save_file.write(temp.head.code, '/ ', temp.head.name, '/ ')
                task = temp.head.head
                # writes the information about the tasks into the file
                while task != None:
                    save_file.write(task.name, ', ', task.desc, ', ', task.start_time, ', ', task.end_time, ', ', task.do_by)
                    # writes a '+ ' if their is anouther task after the current one.
                    if task.next != None:
                        save_file.write('+ ')
                    task = task.next
                # writes a & and new line if their is anouther course after the current one.
                if temp.head.next != None:
                    save_file.write('&\n')
                temp.head = temp.head.next
        return
                
                

    # used to load Courses and their corisponding tasks when the program starts.
    # has no input and returns a list of courses with their tasks.
    def load(self):
        # reads from a text file and changes it into courses and their corresponding tasks
        course_list = Courselist()
        with open(self.file, 'r') as save_file:
            # if file does not exsists return a emty course list.
            if not save_file:
                return course_list
            else:
                i = 0
                course_tasks = None
                file_content = save_file.read()
                # split up the file into nested lists
                course_temp_list = [x.split('/ ') for x in file_content.split('&\n')]
                while i < len(course_temp_list):
                    course_tasks[i] = [x.split(', ') for x in course_temp_list[i][2].split('+ ')]
                    i += 1
                n = 0
                i = 0
                # takes the nested lists and uses it to make a Courselist object
                while n < len(course_temp_list):
                    # creates the Course and puts it in temp.
                    temp = Course(course_temp_list[n][0], course_temp_list[n][1])
                    while i < len(course_tasks):
                        name = course_tasks[i][0]
                        desc = course_tasks[i][1]
                        start_time = course_tasks[i][2]
                        end_time = course_tasks[i][3]
                        do_by = course_tasks[i][4]
                        # takes task part of list and makes a task item of it.
                        temp.add_task(Task(name, desc, start_time, end_time, do_by))
                        i =+ 1
                    course_list.add_task(temp) # addes the temp course to course list.
                    n += 1
        return course_list