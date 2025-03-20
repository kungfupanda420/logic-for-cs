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
    states = [Int(f'step_{i}') for i in range(k + 1)]
    solver.add(states[0] == 0)
    for i in range(k):
        x = states[i]
        y = states[i + 1]
        solver.add(Or(
            And(x == 0, y == 1),
            And(x == 1, y == 0)
        ))
    solver.add(states[k] == 1)
    if solver.check() == sat:
        return True
    else:
        return False

def vending_machine():
    x, y = Ints('x y')
    I = (x == 0)
    T = Or(
        And(x == 0, y == 1),
        And(x == 1, y == 0)
    )
    F = (x == 1)
    return I, T, F

M = vending_machine()
for k in range(1, 5):
    result = FiniteRun(M, k)
    print(f"k = {k}, Result: {result}")