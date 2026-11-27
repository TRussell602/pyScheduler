from pathlib import Path
from objects import Course, Task, Courselist


# the SaveData file holds data in the following form.
# Code/ Name/ name, description, start_time, end_time + name, description, start_time, end_time&
# Code/ Name/ name, description, start_time, end_time + name, description, start_time, end_time

class SaveFile:
    # used to construct the class so load and save are accessible.
    def __init__(self):
        # create a file to hold information about the cources and 
        self.file = Path('../SaveData.txt')

    # used to save the data about Courses and their tasks every time one of them is updated.
    # takes a list of course as input nad returns null.
    def save(self, Course_list): # we may need an object that holds multiple courses
        # writes the course and task data into a test file
        with open(self.file, 'w') as save_file:
            counter = 0
            

        return

    # used to load Courses and their corisponding tasks when the program starts.
    # has no input and returns a list of courses with their tasks.
    def load(self):
        # reads from a text file and changes it into courses and their corresponding tasks
        course_list = Courselist()
        with open(self.file, 'r') as save_file:
            if not save_file:
                return course_list
            else:
                i = 0
                course_tasks = None
                file_content = save_file.read()
                
                course_temp_list = [x.split('/ ') for x in file_content.split('&')]
                while i < len(course_temp_list):
                    course_tasks[i] = [x.split(', ') for x in course_temp_list[i][2].split('+ ')]
                    i += 1
                n = 0
                i = 0
                while n < len(course_temp_list):
                    temp = Course(course_temp_list[n][0], course_temp_list[n][1])
                    while i < len(course_tasks):
                        temp.add_task(Task(course_tasks[i][0], course_tasks[i][1], int(course_tasks[i][2]), int(course_tasks[i][3])))
                        i =+ 1
                    course_list.add_course(temp)
                    n += 1
        return course_list