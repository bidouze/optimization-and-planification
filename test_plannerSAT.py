from plannerSAT_final import *

domain,problem='examples/grapple/grapple.pddl', 'examples/grapple/grapple_pb1.pddl'
planner=plannerSAT()
plan=planner.solve(domain,problem)
valide=planner.check(domain,problem,plan)
if valide:
    print("solution correcte")
else:
    print("solution non valide")
