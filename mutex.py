from z3 import *

def FiniteRun(M, k):
    I, T, F = M
    solver = Solver()
    solver.push()
    solver.add(And(I, F))
    if solver.check() == sat:
        solver.pop()
        return True
    solver.pop()
    states = [(Int(f'p1_step_{i}'), Int(f'p2_step_{i}')) for i in range(k + 1)]
    solver.add(And(states[0][0] == 0, states[0][1] == 0))
    for i in range(k):
        p1_curr, p2_curr = states[i]
        p1_next, p2_next = states[i + 1]
        solver.add(Or(
            And(p1_curr == 0, p2_curr == 0, p1_next == 1, p2_next == 0),
            And(p1_curr == 0, p2_curr == 0, p1_next == 0, p2_next == 1),
            And(p1_curr == 1, p2_curr == 0, p1_next == 2, p2_next == 0),
            And(p1_curr == 0, p2_curr == 1, p1_next == 0, p2_next == 2),
            And(p1_curr == 2, p2_curr == 0, p1_next == 0, p2_next == 0),
            And(p1_curr == 0, p2_curr == 2, p1_next == 0, p2_next == 0)
        ))
    solver.add(And(states[k][0] == 2, states[k][1] == 2))
    if solver.check() == sat:
        return True
    else:
        return False

def mutex_protocol():
    p1, p2 = Ints('p1 p2')
    I = And(p1 == 0, p2 == 0)
    T = Or(
        And(p1 == 0, p2 == 0, p1 == 1, p2 == 0),
        And(p1 == 0, p2 == 0, p1 == 0, p2 == 1),
        And(p1 == 1, p2 == 0, p1 == 2, p2 == 0),
        And(p1 == 0, p2 == 1, p1 == 0, p2 == 2),
        And(p1 == 2, p2 == 0, p1 == 0, p2 == 0),
        And(p1 == 0, p2 == 2, p1 == 0, p2 == 0)
    )
    F = And(p1 == 2, p2 == 2)
    return I, T, F

M = mutex_protocol()
for k in range(1, 5):
    result = FiniteRun(M, k)
    print(f"k = {k}, Result: {result}")