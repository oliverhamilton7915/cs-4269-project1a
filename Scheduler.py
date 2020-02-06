class Scheduler:
    def __init__(self, catalog, goals, initial):
        #
        # catalog: dictionary object holding all course information and prerequisites
        #
        # goals: list object holding all courses necessary for completion by the planner
        #       Note: this object will be dynamically adjusted at runtime. As we 'plan' courses that meet our goals,
        #             we are going to pop() elements from this 'goal' list. See: formulate_schedule() below.
        #
        # initial: list object holding all initially completed courses
        #
        self.catalog = catalog
        self.goal_courses = goals
        self.initial_courses = initial

        # Here we make this into a set for quick lookup
        self.satisfied_prereqs = set(initial)
        self.unsatisfied_prereqs = set(self.goal_courses)

        # Elements will be added to this list as we perform our planning
        self.terms = []

    # This is the method we call from our parent course_scheduler function from in group7_scheduler.py.
    # We want it to start with an initially empty schedule that
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

        flat_schedule = []
        for term_schedule in self.terms:
            for c in term_schedule:
                flat_schedule.append(c)
        return flat_schedule

    # Guidelines:
    # 1. minimum 12 credits/semester, maximum 18 credits/semester
    # 2. schedule should include as few semesters as possible
    # 3. if full schedule cannot fit into 8 total terms (i.e. 4 years college), then we should return None (see spec).
    def formulate_term(self, season, year):
        term_schedule = []
        term_set = set(term_schedule)
        term_credits = 0

        # General workflow idea:
        #   1. make a call to pick_goal_objective - this will return a course we want to consider adding to the schedule
        #   2. See if it is a class (or abstract requirement with 0 associated credits) that can be taken in the current
        #       term. This will be the case if it is a class with no remaining pre-requirements in the current term OR
        #       if it is an abstract course objective (i.e. 0 credits) with all/some pre-requirements in the current
        #       term. If so, add it to the term. Increment credits as necessary and adjust satisfied prereqs.  
        #   3. Otherwise, you will want to call get_minimal_prereqs(class) to see what must be taken before it.
        		# decide whether to handle adding in formulate or in get_minimal credit
        #   4. Those must be pushed to the self.goal_courses stack. If those are pre-requirements to our current
        #       goal course objective, they must be taken first.
        #   5. As long as in each iteration, either (1) a class is removed from the stack and added to term or (2)
        #       a set of pre-requirements for a class are pushed to the stack, we loop in a process where
        #       we build out the rest of the term with useful, satisfiable classes.
        #   6. Lastly, for each class in our term, we want to add that to our set of self.satisfied_prereqs for
        #       reference in later terms where we continue to build out our college schedule.

        possible_course = self.pick_goal_objective(term_schedule)
        course_credits = self.catalog[possible_course].credits
        course_prereqs = self.catalog[possible_course].prereqs
        # Abstract class case: check to see that all prereqs are either in current semester or have already been taken
        # must address case where we have run out of remaining time 
        can_add_class = True
        if course_credits==0:
            for prereq in course_prereqs:
                if prereq not in self.satisfied_prereqs:
                    if prereq not in self.unsatisfied_prereqs:
                        self.get_minimal_prereqs(prereq)
                    can_add_class = False
        else: #not an abstract class
            for prereq in course_prereqs:
                if prereq in term_set or prereq not in self.satisfied_prereqs:
                    can_add_class = False
                if term_credits + course_credits > 18:
                    can_add_class = False
        if can_add_class:
            term_schedule.append(possible_course)
            term_set.add(possible_course)
            self.unsatisfied_prereqs.remove(possible_course)
            self.satisfied_prereqs.add(possible_course)
            self.goal_courses.remove(possible_course)
            term_credits += course_credits
        pass

    # This method will be called from our formulate_term method above when it is looking for a course to either
    #   (1) add to the current term OR
    #   (2) find its pre-requirements to take in the current term
    #   Note: we do not want to return a non-abstract course objective that has its remaining pre-requirements scheduled
    #   in the current term. Why? Well, that course will not be able to fit into the current term because some of its
    #   pre-requirements live in that term. Also, we wont be able to add its pre-requirements to our goal_courses since
    #   they are already in the current term!!
    # it must return the selected goal objective (i.e. ("CS", "4260")) AND it must remove that class from self.goal_courses
    def pick_goal_objective(self, term_schedule):
        #Retrieves the last item in the goal_courses list
        length_goal_courses = len(self.goal_courses)
        found_valid_course = False
        #check for length<1
        while length_goal_courses > 0 and not found_valid_course:
            possible_course = self.goal_courses[length_goal_courses-1]
            course_credits = self.catalog[possible_course].credits
            course_prereqs = self.catalog[possible_course].prereqs
            if course_credits > 0:
                valid = True
                for prereq in course_prereqs:
                    if prereq not in self.satisfied_prereqs:
                        #cant return-preqeqs not already completed
                        valid = False
                if valid:
                    found_valid_course = True
                    return possible_course
                else:
                    length_goal_courses-=1
            else:
                # handle removing from self.goal_courses in above method
                return possible_course
        return None

    # This function gives the minimum set of requirements necessary to allow our enrollment in the goal course
    # It will use self.satisfied_prereqs and self.catalog[goal] to see what options for pre-requirements
    # there are for goal.
    def get_minimal_prereqs(self, goal):
        prereqs = self.catalog[goal].prereqs
        for x in range(len(prereqs)):
            count = 0
            for y in range(len(prereqs[x])):
                if prereqs[x][y] in self.satisfied_prereqs:
                    count += 1
            if count == len(prereqs[x]):
                return []

        min_set_size = 1000
        return_set = []
        for x in range(len(prereqs)):
            count = 0
            prereq_set = []
            for y in range(len(prereqs[x])):
                if prereqs[x][y] in self.satisfied_prereqs:
                    count += 1
                else:
                    prereq_set.append(prereqs[x][y])
            if (len(prereqs[x]) - count) < min_set_size:
                return_set = prereq_set
                min_set_size = (len(prereqs[x]) - count)
        return return_set
