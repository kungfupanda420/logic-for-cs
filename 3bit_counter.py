from z3 import *

def three_bit_counter():
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
        And(x == 7, y == 0))
    F = (x == 7)
    return I, T, F

def FiniteRun(M, k):
    I, T, F = M
    solver = Solver()
    solver.push()
    solver.add(And(I, F))
    if solver.check() == sat:
        solver.pop()
        return True
    solver.pop()
    R = I
    while True:
        Pref1 = And(R, T)
        states = [Int(f'step_{i}') for i in range(k + 1)]
        solver.add(states[0] == 0)
        for i in range(k):
            solver.add(Or(
                And(states[i] == 0, states[i + 1] == 1),
                And(states[i] == 1, states[i + 1] == 2),
                And(states[i] == 2, states[i + 1] == 3),
                And(states[i] == 3, states[i + 1] == 4),
                And(states[i] == 4, states[i + 1] == 5),
                And(states[i] == 5, states[i + 1] == 6),
                And(states[i] == 6, states[i + 1] == 7),
                And(states[i] == 7, states[i + 1] == 0)
            ))
        Suffk0 = (states[-1] == 7)
        solver.push()
        solver.add(Pref1)
        solver.add(Suffk0)
        if solver.check() == sat:
            solver.pop()
            return True if R == I else "Abort"
        else:
            solver.pop()
            return False

M = three_bit_counter()
for k in range(1, 9):
    result = FiniteRun(M, k)
    print(f"k = {k}, Result: {result}")