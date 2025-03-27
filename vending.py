from z3 import *

def FiniteRun(M, k):
    I, T, F = M
    solver = Solver()
    states = [Int(f'step_{i}') for i in range(k + 1)]
    solver.add(substitute(I, (Int('x'), states[0])))
    for i in range(k):
        x = states[i]
        y = states[i + 1]
        solver.add(substitute(T, (Int('x'), x), (Int('y'), y)))
    solver.add(substitute(F, (Int('x'), states[k])))
    if solver.check() == sat:
        print(f"FiniteRun: Property HOLDS for k = {k}")
        print("Model:", solver.model())
        return True
    print(f"FiniteRun: Property FAILS for k = {k}")
    return False


def BMC(M, k):
    I, T, F = M
    solver = Solver()
    states = [Int(f'step_{i}') for i in range(k + 1)]
    solver.add(substitute(I, (Int('x'), states[0])))
    for i in range(k):
        x = states[i]
        y = states[i + 1]
        solver.add(substitute(T, (Int('x'), x), (Int('y'), y)))
    solver.add(Not(substitute(F, (Int('x'), states[k]))))
    if solver.check() == sat:
        print(f"BMC: Counterexample found at k = {k}")
        model = solver.model()
        for i in range(k + 1):
            print(f"Step {i}: {model[states[i]]}")
        return False
    print(f"BMC: Property HOLDS for k = {k}")
    return True


def Interpolation(M, k):
    I, T, F = M
    solver = Solver()
    states = [Int(f'step_{i}') for i in range(k + 1)]
    solver.add(substitute(I, (Int('x'), states[0])))
    for i in range(k):
        x = states[i]
        y = states[i + 1]
        solver.add(substitute(T, (Int('x'), x), (Int('y'), y)))
    solver.add(Not(substitute(F, (Int('x'), states[k]))))
    if solver.check() == unsat:
        print(f"Interpolation: Property HOLDS for k = {k}")
        return True
    print(f"Interpolation: Property FAILS for k = {k}")
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

print("FiniteRun Results")
for k in range(1, 5):
    result = FiniteRun(M, k)
    print(f"k = {k}, Result: {result}")

print("\nBMC Results")
for k in range(1, 5):
    BMC(M, k)

print("\nInterpolation Results")
for k in range(1, 5):
    Interpolation(M, k)
