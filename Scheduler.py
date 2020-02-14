# Group Members
# - Max Cummings
# - Alex Cho
# - Jacob Feldstein
# - Oliver Hamilton

class Scheduler:
    def __init__(self, catalog, goals, initial):

        #
        # catalog: dictionary object holding all course information and prerequisites
        #
        # goal_courses: list object holding all courses necessary for completion by the planner
        #       Note: this object will be dynamically adjusted at runtime. As we 'plan' courses that meet our goals,
        #             we are going to pop() elements from this 'goal' list. See: formulate_schedule() below.
        #
        # initial_courses: list object holding all initially completed courses
        #

        for course in initial + goals:
            assert course in catalog

        self.catalog = catalog
        self.initial_goals = goals
        self.goal_courses = set(goals)
        self.initial_courses = initial

        # Here we make this into a set for quick lookup
        self.satisfied_prereqs = set(initial)

        # Elements will be added to this list as we perform our planning
        self.terms = []

    # This is the method we call from our parent course_scheduler function from in group7_scheduler.py.
    # We want it to start with an initially empty schedule and either return [] if scheduling is impossible,
    # or the schedule if it is possible.
    def formulate_schedule(self):
        assert(len(self.terms) == 0)  # We only want to call this method when we are starting from scratch.
        season = "Spring"
        years = ["Freshman", "Sophomore", "Junior", "Senior"]
        year_index = -1
        while len(self.goal_courses) > 0:
            if season == "Spring" and year_index == 3: # this is after senior spring, we would expect to be graduating!
                return [] # Empty schedule - this is the desired behavior specified by the spec!
            if season == "Spring": # Go to next year
                season = "Fall"
                year_index += 1
            else: # Stay on same year
                season = "Spring"
            self.formulate_term(season, years[year_index])
            if len(self.terms) == 8 and len(self.goal_courses) > 0:
                return []  # if full schedule cannot fit into 8  terms (i.e. 4 years ), then return None (see spec).

        flat_schedule = []
        for term_schedule in self.terms:
            for c in term_schedule:
                flat_schedule.append(c)
        return flat_schedule

    # Season: "Fall" or "Spring"
    # Year: "Freshman", "Sophomore", "Junior", or "Senior"
    # Calling this method adds a term to self.terms which is full of classes that should be taken in that current term
    def formulate_term(self, season, year):
        # Guidelines:
        # 1. maximum 18 credits/semester
        # 2. schedule should include as few semesters as possible
        # 3. if full schedule cannot fit into 8 total terms (i.e. 4 years college), then we should return None (see spec).
        term_schedule = []  # will hold things like (("CS", "1101"), ("Spring", "Freshman"), 3)
        term_set = set()
        unreachable_courses = set()
        term_credits = 0

        # This code of carries out the iterative deepening of the search. Each time we have a non-terminal semester and
        # a non-empty goal_courses set, we pick an item from our fringe of remaining requirements and either add it to
        # or schedule, or pick out its satisfying prereqs to add to our goal_courses set.
        while len(self.goal_courses) > 0:  # while we still have courses to take
            possible_course = self.pick_goal_objective(season)
            course_credits = int(self.catalog[possible_course].credits)
            minimal_course_prereqs = self.get_minimal_prereqs(possible_course)
            if possible_course in self.satisfied_prereqs or possible_course in term_set:
                self.goal_courses.remove(possible_course)
            elif course_credits == 0: # abstract course - split into its components and move on
                self.goal_courses.remove(possible_course)
                self.goal_courses = self.goal_courses.union(set(minimal_course_prereqs))
            elif len(minimal_course_prereqs) > 0: # cannot take class - must take one of its prereqs first
                has_overlapping_course = False
                for pre in minimal_course_prereqs:
                    if pre in term_set or pre in unreachable_courses or pre in self.goal_courses:
                        has_overlapping_course = True
                if has_overlapping_course:
                    unreachable_courses.add(possible_course)
                    self.goal_courses.remove(possible_course)
                    continue
                self.goal_courses = self.goal_courses.union(set(minimal_course_prereqs))
            elif course_credits + term_credits > 18: # cant take class because of capacity reasons
                break  # no more room!
            else:  # can take course - add it to term schedule and perform updates
                self.goal_courses.remove(possible_course)
                term_credits += course_credits
                term_schedule.append((possible_course, (season, year), course_credits))
                term_set.add(possible_course)
                if term_credits == 18:
                    break

        # we want to add back in the nodes we removed from search
        self.goal_courses = self.goal_courses.union(unreachable_courses)

        # now we want to mark this term's courses as prereqs for later reference
        for elem in term_set:
            self.satisfied_prereqs.add(elem)

        # add our term to the overall schedule
        self.terms.append(term_schedule)

    # season: "Fall" or "Spring"
    # This method takes either an abstract course or a course with the lowest number from the fringe (self.goals) and
    # returns that course to the calling method. Here, course number represents our search heuristic.
    def pick_goal_objective(self, season):
        # 1. if there is abstract class return it on sight
        # 2. Otherwise, pick class with lowest possible number. This is our heuristic.
        #   Reason: the courses with the lowest course numbers are the most likely to be the start of course
        #   chains that are the longest and would otherwise prohibit one from graduating on time.

        goal_list = list(self.goal_courses)

        lowest_dept, lowest_course_num = goal_list[0]
        for course in goal_list:
            if season not in self.catalog[course].terms:
                continue
            if not course[1][:-1].isnumeric():  # chop off last character because of writing courses (i.e. 1200W)
                return course
            if course[1] < lowest_course_num:
                lowest_course_num = course[1]
                lowest_dept = course[0]
        return lowest_dept, lowest_course_num

    # goal: course tuple (i.e. ("CS","2201")
    # This function gives the minimum set of requirements necessary to allow our enrollment in the goal course.
    # It does so by cross referencing self.satisfied_prereqs with the DNF prereq options enumerated in self.catalog
    def get_minimal_prereqs(self, goal):
        dnf = self.catalog[goal].prereqs
        if goal[1][:4] == "open" or goal[1][:7] == "science" or goal[1][:10] == "depthother":
            # We enter this block of code when we are trying to get the minimum prereqs for
            # an an abstract course bucket that cannot have prereqs currently contained in our self.goal_objectives
            i = 0
            while dnf[i][0] in self.goal_courses:
                i += 1
            return dnf[i]
        if len(dnf) > 0:
            best_option = dnf[0]
            for option in dnf:
                challenger = []
                for c in option:
                    if c not in self.satisfied_prereqs:
                        challenger.append(c)
                if len(challenger) < len(best_option):
                    best_option = challenger
            return best_option
        return []

    # this method clears the schedule computed by the scheduler
    def clear_scheduler(self):
        self.terms = []
        self.satisfied_prereqs = set(self.initial_courses)
        self.goal_courses = set(self.initial_goals)
