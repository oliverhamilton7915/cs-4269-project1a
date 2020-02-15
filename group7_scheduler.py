# Group Members
# - Max Cummings
# - Alex Cho
# - Jacob Feldstein
# - Oliver Hamilton

import time
import sys
import course_dictionary
from Scheduler import Scheduler

def main(argv):

   # Here is the course catalog that is made from reading
   # the excel sheet, CourseCatalogSpring2020.xlsx
   #
   # Check out course_dictionary.py to see how that was done.
   # That code was provided to us.

   print("Creating Course catalog...")
   print()
   course_dict = course_dictionary.create_course_dict()

   # Test code to help visualize what each call returns
   # calc = course_dict[('CS', 'calculus')]
   # print(calc.prereqs)
   # print(len(calc.prereqs))
   # print(calc.prereqs[0])
   # print(len(calc.prereqs[0]))
   # print(calc.prereqs[0][0])

   # Code Example 1: printing all CS Courses.
   #
   # for course in course_dict:
   #     if course.program == 'CS':
   #         print(course, course_dict[course])
   #
   # NOTE: this is a series of print statements representing (key, value) pairs. the key is the course formatted like:
   #   Course(program='CS', designation='3860'). The value is the information associated with that course. Formatted:
   #   CourseInfo(credits=3, terms=('Spring', 'Fall'), prereqs=((('CS', '2231'),),))
   #
   #   Check example two to see this in greater detail.
   #
   # --Output--:
   # Course(program='CS', designation='3860') CourseInfo(credits=3, terms=('Spring', 'Fall'), prereqs=((('CS', '2231'),),))
   # Course(program='CS', designation='3861') CourseInfo(credits=3, terms=('Summer', 'Spring', 'Fall'), prereqs=((('CS', '2231'),),))
   # Course(program='CS', designation='3892') CourseInfo(credits=3, terms=('Spring', 'Fall'), prereqs=())
   # Course(program='CS', designation='3890') CourseInfo(credits=3, terms=('Summer',), prereqs=())
   # Course(program='CS', designation='3891') CourseInfo(credits=3, terms=('Fall',), prereqs=())
   # ...
   # ...

   # Code Example 2: printing select courses and their properties
   #
   # cs3251 = course_dict[('CS', '3251')]
   # print(cs3251)
   # print(cs3251.credits)
   # print(cs3251.terms)
   # print(cs3251.prereqs)
   #
   # --Output--:
   # CourseInfo(credits='3', terms=('Spring', 'Fall'), prereqs=((('CS', '2201'),),))
   # 3
   # ('Spring', 'Fall')
   # ((('CS', '2201'),),)
   print("Running tests...")
   print()
   # See if all prerequirements (prereq) are in the file.
   assert(len(get_unsatisfied_prereqs(course_dict)) == 0)
   # See if all courses have a term and credits
   assert(len(get_ambiguous_courses(course_dict)) == 0)
   #Test1-3: See if we properly recognize impossible scheduling objectives
   assert(check_proper_scheduling(course_dict))
   #See if there are no more than 18 hours in each semester
   assert(check_correct_hours(course_dict, [("CS","major"), ("MATH","4650")]))
   assert(check_correct_hours(course_dict, [("CS","major")]))
   #Test4-6: to see if the initial courses properly work
   assert(check_with_initials(course_dict))

   print("Performing course search...")
   print()

   # --- INPUT INFORMATION ---

   goal_conditions = [("CS", "major")]
   initial_state = []

   # --- END INPUT INFO ---

   print("Search goals: ")
   for (dept, c) in goal_conditions:
       print(dept + ' ' + c)
   print()
   print("Initial states: ")
   for (dept, c) in initial_state:
       print(dept + ' ' + c)
   print()

   start_time = time.time()
   schedule = course_scheduler(course_dict, goal_conditions, initial_state)
   run_time_ms = 1000 * (time.time() - start_time)

   print("Scheduler ran in " + str(run_time_ms) + "ms")
   print()
   print("Schedule output: ")
   print()
   pretty_print(schedule)

# ---SCHEDULER CODE---:

# course_descriptions: dictionary object holding all course information and prerequisites
# goal_conditions: list object holding all courses
# initial_state: list object holding all completed courses
def course_scheduler(course_descriptions, goal_conditions, initial_state):
   schedule = Scheduler(course_descriptions, goal_conditions, initial_state)
   return schedule.formulate_schedule()

# schedule: list of ((department, course), (year, term), credit hours) tuples
def pretty_print(schedule):
   for ((debt, num), (season, year), credits) in schedule:
       print("Course: " + debt + " " + num + ", Term: " + year + " " + season + ", Credits: " + str(credits))

# ---TESTS---:

def get_unsatisfied_prereqs(course_dict):
   unsatisfied_prereqs = []
   prereq_list = [single_course for vals in course_dict.values()
                  for some_prereqs in vals.prereqs for single_course in some_prereqs]
   for prereq in prereq_list:
       if prereq not in course_dict:
           unsatisfied_prereqs.append(prereq)
   return unsatisfied_prereqs

def get_ambiguous_courses(course_dict):
   ambiguous_courses = []
   for key in course_dict:
       #Test to see if every course has a term and credits.
       if not course_dict[key].terms or not course_dict[key].credits:
           ambiguous_courses.append(key)
       #Test to see if a course's prereqs include the course itself
       if key in [course for prereq in course_dict[key].prereqs for course in prereq]:
           ambiguous_courses.append(key)
   return ambiguous_courses

def check_proper_scheduling(course_dict):

   # We should be able to complete this
   test_schedule1 = course_scheduler(course_dict, [("CS","major")], [])
   len_schedule1 = len(test_schedule1)

   #Test1: Impossible schedule goals
   # We should NOT be able to complete this
   start_time = time.time()
   test_schedule2 = course_scheduler(course_dict, [("CS","major"), ("MATH","4650"), ("BME","3300")], [])
   run_time_ms = 1000 * (time.time() - start_time)
   print("Test 1 ran in " + str(run_time_ms) + "ms")
   len_schedule2 = len(test_schedule2)

   #Test2: Zero goals
   start_time = time.time()
   test_schedule3 = course_scheduler(course_dict, [], [])
   run_time_ms = 1000 * (time.time() - start_time)
   print("Test 2 ran in " + str(run_time_ms) + "ms")
   len_schedule3 = len(test_schedule3)

   #Test3: No Prereqs for goal
   start_time = time.time()
   test_schedule4 = course_scheduler(course_dict, [("CS","1101")], [])
   run_time_ms = 1000 * (time.time() - start_time)
   print("Test 3 ran in " + str(run_time_ms) + "ms")
   len_schedule4 = len(test_schedule4)

   return len_schedule1 > 0 and len_schedule2 == 0 and len_schedule3 == 0 and len_schedule4 == 1

def check_correct_hours(course_dict, goals):
   test_schedule1 = Scheduler(course_dict, goals, []) # We should be able to complete this objective
   schedule1 = test_schedule1.formulate_schedule()
   num_hours = 0
   semester = ('Fall', 'Freshman')
   for course in schedule1:
       if course[1] == semester:
           num_hours += course[2]
       else:
           if num_hours > 18:
             return False
           num_hours = course[2]
           semester = course[1]

   return num_hours < 18 # Make sure the last semester does not go over 18 hours either


def check_with_initials(course_dict):
   #Test4: Initial classes satisfy the prerequisites for the goal
   start_time = time.time()
   schedule1 = course_scheduler(course_dict, [("MATH","4650")], [("MATH","2810"), ("MATH","3650"), ("MATH","3640")])
   run_time_ms = 1000 * (time.time() - start_time)
   print("Test 4 ran in " + str(run_time_ms) + "ms")
   test1 = schedule1 == [(('MATH', '4650'), ('Fall', 'Freshman'), 3)]

   #Test5: Initial classes are the goal
   start_time = time.time()
   schedule2 = course_scheduler(course_dict, [("MATH","4650")], [("MATH","4650")])
   run_time_ms = 1000 * (time.time() - start_time)
   print("Test 5 ran in " + str(run_time_ms) + "ms")
   test2 = schedule2 == []

   #Test6: Irrelevent initial courses should not change the schedule
   schedule4 = course_scheduler(course_dict, [("CS", "major")], [])
   start_time = time.time()
   schedule5 = course_scheduler(course_dict, [("CS", "major")],
                                [("ECON", "1111"), ("FREN", "1111"), ("HOD", "1690")])
   run_time_ms = 1000 * (time.time() - start_time)
   print("Test 6 ran in " + str(run_time_ms) + "ms")
   test3 = len(schedule5) == len(schedule4)

   return test1 and test2 and test3

if __name__ == "__main__":
   main(sys.argv)




























