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
    
    states = [(Bools(f'p1_0_{i} p1_1_{i} p1_2_{i}') + Bools(f'p2_0_{i} p2_1_{i} p2_2_{i}')) for i in range(k + 1)]
    
    solver.add(And(states[0][0], states[0][3]))
    
    for i in range(k):
        p1, p2 = states[i], states[i + 1]
        solver.add(Or(
            And(p1[0], p1[3], p2[1], p2[3]),
            And(p1[0], p1[3], p2[0], p2[4]),
            And(p1[1], p1[3], p2[2], p2[3]),
            And(p1[0], p1[4], p2[0], p2[5]),
            And(p1[2], p1[3], p2[0], p2[3]),
            And(p1[0], p1[5], p2[0], p2[3])
        ))
    
    solver.add(And(states[k][2], states[k][5]))
    
    if solver.check() == sat:
        return True
    return False

def BMC(M, k):
    I, T, F = M
    solver = Solver()
    
    states = [(Bools(f'p1_0_{i} p1_1_{i} p1_2_{i}') + Bools(f'p2_0_{i} p2_1_{i} p2_2_{i}')) for i in range(k + 1)]
    
    solver.add(And(states[0][0], states[0][3]))
    
    for i in range(k):
        p1, p2 = states[i], states[i + 1]
        solver.add(Or(
            And(p1[0], p1[3], p2[1], p2[3]),
            And(p1[0], p1[3], p2[0], p2[4]),
            And(p1[1], p1[3], p2[2], p2[3]),
            And(p1[0], p1[4], p2[0], p2[5]),
            And(p1[2], p1[3], p2[0], p2[3]),
            And(p1[0], p1[5], p2[0], p2[3])
        ))
    
    solver.add(Not(And(states[k][2], states[k][5])))
    
    if solver.check() == sat:
        print(f"BMC: Counterexample found at k = {k}")
        model = solver.model()
        for i in range(k + 1):
            p1_state = [model[states[i][j]] for j in range(3)].index(True)
            p2_state = [model[states[i][j + 3]] for j in range(3)].index(True)
            print(f"Step {i}: p1 = {p1_state}, p2 = {p2_state}")
        return False
    print(f"BMC: Property HOLDS for k = {k}")
    return True

def Interpolation(M, k):
    I, T, F = M
    solver = Solver()
    
    states = [(Bools(f'p1_0_{i} p1_1_{i} p1_2_{i}') + Bools(f'p2_0_{i} p2_1_{i} p2_2_{i}')) for i in range(k + 1)]
    
    solver.add(And(states[0][0], states[0][3]))
    
    for i in range(k):
        p1, p2 = states[i], states[i + 1]
        solver.add(Or(
            And(p1[0], p1[3], p2[1], p2[3]),
            And(p1[0], p1[3], p2[0], p2[4]),
            And(p1[1], p1[3], p2[2], p2[3]),
            And(p1[0], p1[4], p2[0], p2[5]),
            And(p1[2], p1[3], p2[0], p2[3]),
            And(p1[0], p1[5], p2[0], p2[3])
        ))
    
    solver.add(Not(And(states[k][2], states[k][5])))
    
    if solver.check() == unsat:
        print(f"Interpolation: Property HOLDS for k = {k}")
        return True
    print(f"Interpolation: Property FAILS for k = {k}")
    return False

def mutex_protocol():
    I = True
    T = True
    F = True
    return I, T, F

M = mutex_protocol()

print("=== FiniteRun Results ===")
for k in range(1, 5):
    result = FiniteRun(M, k)
    print(f"k = {k}, Result: {result}")

print("\n=== BMC Results ===")
for k in range(1, 5):
    BMC(M, k)

print("\n=== Interpolation Results ===")
for k in range(1, 5):
    Interpolation(M, k)
