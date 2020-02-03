# Group Members
# - Max Cummings
# - Alex Cho
# - Jacob Feldstein
# - Oliver Hamilton

import sys
import course_dictionary

def main(argv):

    # Here is the course catalog that is made from reading
    # the excel sheet, CourseCatalogSpring2020.xlsx
    #
    # Check out course_dictionary.py to see how that was done.
    # That code was provided to us.
    course_dict = course_dictionary.create_course_dict()

    # Code Example 1: printing all CS Courses.
    #
    # for course in course_dict:
    #     if course.program == 'CS':
    #        print(course, course_dict[course])
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

    # Test1: to see if all prerequirements (prereq) are in the file.
    assert(len(get_unsatisfied_prereqs(course_dict)) == 0)

    # Test2: to see if all courses have a term and credits
    assert(len(get_ambiguous_courses(course_dict)) == 0)


# ---SCHEDULER CODE---:

# course_descriptions: dictionary object holding all course information and prerequisites
# goal_conditions: list object holding all courses
# initial_state: list object holding all completed courses
def course_scheduler(course_descriptions, goal_conditions, initial_state):
    pass

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

if __name__ == "__main__":
    main(sys.argv)