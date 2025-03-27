from z3 import *

def get_model_2bit():
    I = [False, False]
    def T(x, y):
        x_bv = Sum([If(x[j], 2**j, 0) for j in range(2)])
        y_bv = Sum([If(y[j], 2**j, 0) for j in range(2)])
        return y_bv == (x_bv + 1) % 4
    def F(y):
        return And([y[j] == True for j in range(2)])
    return (I, T, F)

def FiniteRun(M, k):
    I, T, F = M
    solver = Solver()
    states = [[Bool(f'step_{i}_b{j}') for j in range(2)] for i in range(k + 1)]
    for j in range(2):
        solver.add(states[0][j] == I[j])
    for i in range(k):
        solver.add(T(states[i], states[i + 1]))
    solver.add(F(states[k]))
    if solver.check() == sat:
        print(f"FiniteRun (k={k}): Reaches 11")
    else:
        print(f"FiniteRun (k={k}): Does not reach 11")

def BMC(M, max_k):
    I, T, F = M
    for k in range(1, max_k + 1):
        solver = Solver()
        states = [[Bool(f'step_{i}_b{j}') for j in range(2)] for i in range(k + 1)]
        for j in range(2):
            solver.add(states[0][j] == I[j])
        for i in range(k):
            solver.add(T(states[i], states[i + 1]))
        violation_found = False
        for i in range(1, k + 1):
            solver.push()
            solver.add(F(states[i]))
            if solver.check() == sat:
                print(f"BMC found violation at step {i} (within k={k})")
                violation_found = True
                solver.pop()
                break
            solver.pop()
        if violation_found:
            return
    print(f"BMC completed (k={max_k}): No violation found")

def Interpolation(M, max_k):
    I, T, F = M
    s = Solver()
    current_approx = I
    reached_fixed_point = False
    for k in range(1, max_k + 1):
        states = [[Bool(f'step_{i}_b{j}') for j in range(2)] for i in range(k + 1)]
        s.reset()
        for j in range(2):
            s.add(states[0][j] == current_approx[j])
        for i in range(k):
            s.add(T(states[i], states[i + 1]))
        s.push()
        s.add(F(states[k]))
        if s.check() == sat:
            print(f"interpolation (k={k-1}): Reaches 11")
            return
        s.pop()
        new_approx = [Or(current_approx[j], states[k][j]) for j in range(2)]
        if current_approx == new_approx:
            reached_fixed_point = True
            print("interpolation:reached")
            break
        current_approx = new_approx
    if not reached_fixed_point:
        print(f"Interpolation: No conclusion within {max_k} steps")

def main():
    M = get_model_2bit()
    max_k = 5
    print("2-bit binary counter Verification")
    print("\nfinite run verification:")
    for k in range(1, max_k + 1):
        FiniteRun(M, k)
    print("\nbounded model checking:")
    BMC(M, max_k)
    print("\ninterpolation-based verification:")
    Interpolation(M, max_k)

if __name__ == "__main__":
    main()