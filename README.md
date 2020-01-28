# cs-4269-project1a
You will create the backbone of the intelligent curriculum advisor. Submit a Python file (<yourname>_scheduler.py, e.g., dougfisher_scheduler.py) that implements a (heuristic) depth-first, regression scheduler that achieves a goal set of requirements. The top-level function that you will implement is

def course_scheduler (course_descriptions, goal_conditions, initial_state)

where the arguments and return type are explained below, along with other needed background. In what follows, I have used ‘( )’ to indicate when order of the elements is important (i.e., tuples) and ‘[ ]’ when the order of elements is not important (i.e., a list), but you might choose an implementation in which tuples are implemented as Python lists, or vice versa.

A) For purposes of this project, a course is represented by two strings (<program>, <designation>), such as (“CS” “4260”), (“CS” “3265”), (“HIST” “2640”), (“CHEM”, “3135W”).

B) Each course is associated with a course description, which for purposes of this project, is limited to number of credits, terms in which the course is offered, and prerequisites of the course. For example, the description of (“CS”, “4260”) is ((“CS”, “4260”), 3, (“Fall”), [[(“CS”, “3250”) and (“CS”, “3251”)]]), and the description of (“CS”, “1101”) is ((“CS”, “1101”), 3, (“Fall”, “Spring”), [ ]).

You are provided with a customized Vanderbilt course catalog and code that translates a csv file of this information, for almost all Vanderbilt courses, into a Python (3) dictionary, which is the course_descriptions argument to course_scheduler function.

C) A scheduled term is represented by a pair of strings, such as (“Fall”, “Frosh”), (“Spring”, “Soph”), (“Fall”, “Junior”), and (“Spring”, “Senior”). You won’t be creating a schedule for specific years (e.g., 2012 – 2016), but for frosh-senior (or less, if the requirements can be completed in less than 4 years).

D) A scheduled course is a triple containing a course, a scheduled term, and a number of credits, such as ((“CS”, “2201”), (“Spring”, “Frosh”), 3).

E) There are higher level requirements for different majors and minors too, which are also represented by a pair of strings, such as (“CS”, “mathematics”), which represents the mathematics requirements for a CS major.
Records for higher level requirements are also be stored in the course_descriptions dictionary, but there these requirements can be completed (in theory) during any term, and these higher level requirements add 0 (zero) additional credits beyond the course credits. So, for example, the “course” description representing the higher level requirement (“CS”, “mathematics”) is ((“CS”, “mathematics”), 0, (“Fall”, “Spring”), …). A scheduled course representing a higher level requirement might be ((“CS”, “mathematics”), (“Fall”, “Junior”), 0).

F) Courses and high level requirements have zero or more listed prerequisites. For example, using a format close to that given in the Vanderbilt course catalog

1. (“CS”, “1101”) has no prerequisites.
2. (“CS”, “3270”) has a single listed prerequisite of (“CS”, “2231”).
3. (“CS”, “4260”) has a conjunction of two prerequisites (i.e., [(“CS”, “3250”) and (“CS”, “3251”)]).
4. (“CS”, “4283”) has a disjunction of two prerequisites (i.e., [(“CS”, “3281”) or (“EECE”, “4376”])).
5. (“CS”, “3258”) has a combination of conjunction and disjunction (i.e., [[(“MATH”, “2410”) or (“MATH”, “2400”) or (“MATH”, “2501”) or (“MATH”, “2600”)] and (“CS”, “3251”)]).
6. (“CS”, “mathematics”) has “prerequisites” of [(“CS”, “calculus”) and (“CS”, “stats-probability”) and (“CS”, “math-elective”)].
7. In turn, (“CS”, “calculus”) has prerequisites that are stated as
[ [(“MATH”, “1200”) and (“MATH”, “1201”) and (“MATH”, “1301”) and (“MATH”, “2300”)] and [(“MATH”, “2410”) or (“MATH”, “2600”)]]
or
[[ (“MATH”, “1300”) and (“MATH”, 1301) and (“MATH”, “2300”)] and [(“MATH”, “2410”) or (“MATH”, “2600”)]]
or
[(“MATH”, “1300”) and (“MATH”, “1301”) and (“MATH”, “2500”) and (“MATH”, “2501”)]
8. (“CS”, “major”) has prerequisites
[(“CS”, “mathematics”) and (“CS”, “science”) and (“ES”, “1401”) and (“ES”, “1402”) and (“ES”, “1403”) and (“Eng”, “liberalartscore”) and (“CS”, “core”) and (“CS”, “depth”) and (“CS”, “4959”) and (“CS”, “technicalelectives”) and (“CS”, “openelectives”) and (“CS”, “writingrequirement”)]

G) Each requirement’s prerequisites will be provided in disjunctive normal form, given as a list of lists of subordinate requirements. For example,
1. the (“CS”, “calculus”) prerequisites will actually be given to the planner as
[ [(“MATH”, “1200”) and (“MATH”, “1201”) and (“MATH”, “1301”) and (“MATH”, “2300”) and (“MATH”, “2410”)]
or [(“MATH”, “1200”) and (“MATH”, “1201”) and (“MATH”, “1301”) and (“MATH”, “2300”) and (“MATH”, “2600”)]
or [(“MATH”, “1300”) and (“MATH”, “1301”) and (“MATH”, “2300”) and (“MATH”, “2410”) ]
or [(“MATH”, “1300”) and (“MATH”, “1301”) and (“MATH”, “2300”) and (“MATH”, “2600”) ]
or [(“MATH”, “1300”) and (“MATH”, “1301”) and (“MATH”, “2500”) and (“MATH”, “2501”)] ]

Because the ‘or’s and ‘and’s are implicit in the nesting of a DNF structures, we can simply with this as a list of lists, without the logical keywords. So, the abbreviated DNF representation of the (“CS”, “calculus”) prerequisites can be written as

[ [(“MATH”, “1200”), (“MATH”, “1201”), (“MATH”, “1301”), (“MATH”, “2300”), (“MATH”, “2410”)]
, [(“MATH”, “1200”), (“MATH”, “1201”), (“MATH”, “1301”), (“MATH”, “2300”), (“MATH”, “2600”)]
, [(“MATH”, “1300”), (“MATH”, “1301”), (“MATH”, “2300”), (“MATH”, “2410”) ]
, [(“MATH”, “1300”), (“MATH”, “1301”), (“MATH”, “2300”), (“MATH”, “2600”) ]
, [(“MATH”, “1300”), (“MATH”, “1301”), (“MATH”, “2500”), (“MATH”, “2501”) ] ]

ii) The (“CS”, “3258”) prerequisites in DNF would be given as
[ [(“MATH”, “2400”), (“CS”, “3251”)],
[(“MATH”, “2501”), (“CS”, “3251”)],
[(“MATH”, “2600”), (“CS”, “3251”)] ]

iii) The (“CS”, “4260”) prerequisites would be given as [ [(“CS”, “3250”), (“CS”, “3251”)] ] (i.e., a disjunctive statement with only one conjunctive element)

iii) The (“CS”, “4283”) prerequisites would be given as [ [(“CS”, “3281”)], [(“EECE”, “4376”)] ] (i.e., a disjunction of two one-element conjunctions)

iv) The (“CS”, “3270”) prerequisites are [ [(“CS”, “2231”)] ]

v) The (“CS”, “1101”) prerequisites are [ ]

H) Each state in the state space of the regression planner is a conjunction of courses and/or higher-level requirements, such as
[ (“CS”, “2201”) and … and (“CS”, “technicalelectives”) and … and
(“MATH”, “2410”) ]
or written in strict list form as
[ (“CS”, “2201”), …, (“CS”, “technicalelectives”), …, (“MATH”, “2410”) ]
In a regression planner, this represents a set of conditions (subgoals) that are to be achieved

I) The initial state for the regression planner, an argument to the course_scheduler function, are the courses for which a student already has credit when the planner is executed. Formally, this is a conjunction of courses. For this project assume that the initial state does not include higher level requirements. For example, a student with AP credit for introductory Spanish and introductory programming, would have an initial state of [(“SPAN”, “1101”), (“CS”, “1101”)]. Note that the initial state is not the same as the start state (or start node or root of the search tree) of the regression planner — see section 6.3 of the textbook for clarity on the meaning of terms.

J) Goal conditions, an argument to the course_scheduler function, indicates specific courses and higher-level requirements that the student wants to satisfy. In a curriculum planner, these would typically correspond to the requirements of one or more majors (and minors), but the goal specification could be composed of any courses and high level requirements. For this project, assume that the goal conditions are given as a conjunction of courses and/or higher level requirements.
For example, the goal specification for a CS student in the Engineering School, who wanted to double major in biological sciences, and wanted to be be sure to have the AI project course and science fiction, might be

[(“CS”, “major”), (“BSCI”, “major”), (“CS”, “4269”), (“ENGL”, “3728W”)]

K) Each operator, O, has the form ((PRE(O), EFF(O)), ScheduledTerm, credits), where EFF(O) is a single course that will be added to the student’s transcript if the conjunction of prerequisite courses in PRE(O) are satisfied. When an operator is added by the regression planner it will also have a scheduled term associated with it (e.g., (Fall, Senior) and the number of credits that are added).

L) During planning, your system will instantiate the operator template (which you will define in your Python implementation) to construct actual operators based on information about the prerequisites of courses and the terms they are to be taken.
So, for example, an operator for adding (“CS”, “4260”) to the schedule might be
([(“CS”, “3250”), (“CS”, “3251”)], (“CS”, “4260”), (“Spring”, “Junior”), 3).
An operator for adding (“CS”, “1101”) to the schedule might be
([ ], (“CS”, “1101”), (“Fall”, “FROSH”), 3).
For an operator that expands a higher level requirement

M) A plan is a conjunction of scheduled courses, with constraints that (a) the sum of the credits in each scheduled term (e.g., (“Spring”, “Soph”)) must not be less than 12 and must not be greater than 18.; and (b) no course can be planned for a term that occurs before the term that a pre-requisite is planned. The function course_scheduler will be returning a plan.

N) If the conditions of the goal cannot be satisfied in four years under the constraints above, then the scheduler should return ( ) — the empty conjunction

O) In addition to code for translating files to dictionaries, we may distribute other skeletal code for preprocessing and post-processing your results. We will also translate the CS major requirements of f(viii) above into the requisite form, and you will be required to translate at least one other major requirements. (removed 10/18/17, but can be used as a low-weight addition in second deliverable of Nov 29)

P) In the course catalog there are numerous special kinds of prerequisites, such as “18 – 20 hours” of Open Electives. We will simplify the problem by removing such constraints, and always express prerequisites as DNF of courses and higher level requirements. But in some cases it is desirable to have a generalized course that can be instantiated in different ways. For example, (“CS”, “????”) will match any CS course or CS higher level requirement. (“CS”, “4???”) will match any 4000 level CS course. (“?”, “????”) will match any course offered at Vanderbilt. So, for example, (“CS”, “openelectives”) might have prerequisites [ [(“?”, “????”), (“?”, “????”), (“?”, “????”), (“?”, “????”), (“?”, “????”), (“?”, “????”)] ].
Asking you to implement this pattern matching capability, and more onerously, to search using it, where a pattern could match any course in the catalog, would likely lead to more expensive searches than we are willing to tolerate for grading. There are more elegant solutions, which I hope we talk about, but we will always translate the prerequisites of requirements into DNF expressions of ground courses — no pattern matching required. When you translate an additional major, you will follow the same guidelines for simplifying the problem.

Q) There are other characteristics of your planner that we will measure, such as the length of plans on sample problems

R) Again, your implementation is to be a (heuristic) depth-first, regression planner that adheres to the def course_scheduler (course_descriptions, goal_conditions, initial_state) at the top level. But you have considerable freedom in designing the system, to include class definitions that are used internally by your system. For example, if you aspire to implement composite (macro) learning if a subsequent implementation, you could define the EFFects list of operators as a list of courses rather than a single course INTERNALLY, even if on your initial submission will assume that a plan of operators is produced with a singleton EFFect for each operator.

Whatever your design, it should adhere roughly to the implementation of the generic search algorithm of Poole and McWorth Section 3.4 (http://artint.info/2e/html/ArtInt2e.Ch3.S4.html) or Russell and Norvig as a depth-first search, and a backward or regression search implementation of a scheduler, as addressed in sections 3.8.2 (http://artint.info/2e/html/ArtInt2e.Ch3.S8.SS2.html) and 6.3 (http://artint.info/2e/html/ArtInt2e.Ch6.S3.html), or corresponding sections of Russell and Norvig.
