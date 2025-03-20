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
            And(x == 1, y == 2),
            And(x == 2, y == 3),
            And(x == 3, y == 4),
            And(x == 4, y == 5),
            And(x == 5, y == 6),
            And(x == 6, y == 7),
            And(x == 7, y == 8),
            And(x == 8, y == 9),
            And(x == 9, y == 10),
            And(x == 10, y == 11),
            And(x == 11, y == 12),
            And(x == 12, y == 13),
            And(x == 13, y == 14),
            And(x == 14, y == 15),
            And(x == 15, y == 0)
        ))
    solver.add(states[k] == 15)
    if solver.check() == sat:
        return True
    else:
        return False

def four_bit_counter():
    x, y = Ints('x y')
    I = (x == 0)
    T = Or(
        And(x == 0, y == 1),
        And(x == 1, y == 2),
        And(x == 2, y == 3),
        And(x == 3, y == 4),
        And(x == 4, y == 5),
        And(x == 5, y == 6),
        And(x == 6, y == 7),
        And(x == 7, y == 8),
        And(x == 8, y == 9),
        And(x == 9, y == 10),
        And(x == 10, y == 11),
        And(x == 11, y == 12),
        And(x == 12, y == 13),
        And(x == 13, y == 14),
        And(x == 14, y == 15),
        And(x == 15, y == 0)
    )
    F = (x == 15)
    return I, T, F

M = four_bit_counter()
for k in range(1, 16):
    result = FiniteRun(M, k)
    print(f"k = {k}, Result: {result}")