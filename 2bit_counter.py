from z3 import *

def FiniteRun(M, k):
    I, T, F = M
    solver = Solver()
    states = [Int(f"step_{i}") for i in range(k + 1)]
    solver.add(substitute(I, (x, states[0])))
    for i in range(k):
        solver.add(substitute(T, (x, states[i]), (y, states[i+1])))
    solver.add(substitute(F, (x, states[k])))
    if solver.check() == sat:
        return True
    else:
        return False

x, y = Ints('x y')
I = (x == 0)
T = Or(
    And(x == 0, y == 1),
    And(x == 1, y == 2),
    And(x == 2, y == 3),
    And(x == 3, y == 0)
)
F = (x == 3)
M = (I, T, F)

for k in range(1, 5):
    result = FiniteRun(M, k)
    print(f"k = {k}, Result: {result}")