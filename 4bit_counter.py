from z3 import *

def get_model():
    I = [False, False, False, False]  # Initial state (0 in binary)

    def T(x, y):
        """Transition relation: x -> y (increment by 1 in 4-bit binary)."""
        x_bv = Sum([If(x[j], 2**j, 0) for j in range(4)])
        y_bv = Sum([If(y[j], 2**j, 0) for j in range(4)])
        return y_bv == (x_bv + 1) % 16

    def F(y):
        """Final state: all bits set to 1 (binary 15)."""
        return And([y[j] == True for j in range(4)])

    return (I, T, F)

def FiniteRun(M, k):
    I, T, F = M
    solver = Solver()

    states = [[Bool(f'step_{i}_b{j}') for j in range(4)] for i in range(k + 1)]

    # Initial state
    for j in range(4):
        solver.add(states[0][j] == I[j])

    # Transition relation
    for i in range(k):
        x = states[i]
        y = states[i + 1]
        solver.add(T(x, y))

    # Final state check (always enforce F at step k)
    solver.add(F(states[k]))

    if solver.check() == sat:
        print(f"FiniteRun: Property HOLDS for k = {k}")
        return True
    else:
        print(f"FiniteRun: Property FAILS for k = {k}")
        return False

def BMC(M, k):
    I, T, F = M
    solver = Solver()

    states = [[Bool(f'step_{i}_b{j}') for j in range(4)] for i in range(k + 1)]

    for j in range(4):
        solver.add(states[0][j] == I[j])

    for i in range(k):
        x = states[i]
        y = states[i + 1]
        solver.add(T(x, y))

    # Always enforce F at step k
    solver.add(F(states[k]))

    if solver.check() == sat:
        print(f"BMC: Property HOLDS for k = {k}")
        return True
    else:
        print(f"BMC: Property FAILS for k = {k}")
        return False

def Interpolation(M, k):
    I, T, F = M
    solver = Solver()

    states = [[Bool(f'step_{i}_b{j}') for j in range(4)] for i in range(k + 1)]

    for j in range(4):
        solver.add(states[0][j] == I[j])

    for i in range(k):
        x = states[i]
        y = states[i + 1]
        solver.add(T(x, y))

    # Always enforce F at step k
    solver.add(F(states[k]))

    if solver.check() == sat:
        print(f"Interpolation: Property HOLDS for k = {k}")
        return True
    else:
        print(f"Interpolation: Property FAILS for k = {k}")
        return False

def main():
    M = get_model()
    max_k = 16
    for k in range(1, max_k + 1):
        FiniteRun(M, k)
        BMC(M, k)
        Interpolation(M, k)

if __name__ == "__main__":
    main()