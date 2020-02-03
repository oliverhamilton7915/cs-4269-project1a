class Scheduler:
    def __init__(self, catalog, goals, initial):
        # catalog: dictionary object holding all course information and prerequisites
        # goals: list object holding all courses necessary for completion by the planner
        # initial: list object holding all initially completed courses
        self.catalog = catalog
        self.goal_courses = goals
        self.initial_courses = initial

        # Here we make this into a set for quick lookup
        self.satisfied_prereqs = set(initial)

        # Elements will be added to this list as we perform our planning
        self.schedule = []

    # This function gives the minimum set of requirements necessary to allow our enrollment in the goal course
    # It will use self.satisfied prereqs and self.catalog[goal] to see what options for prereqs there are for goal.
    def get_minimal_prereqs(self, goal):
        pass

    # Guidelines:
    # 1. minimum 12 credits/semester, maximum 18 credits/semester
    # 2. schedule should include as few semesters as possible
    # 3. if full schedule cannot fit into 8 total terms (i.e. 4 years in college), then we should return None (see spec).
    def add_to_schedule(self, course):
        pass