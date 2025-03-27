from z3 import *

def get_model_3bit():
    I = [False, False, False]
    
    def T(x, y):
        x_bv = Sum([If(x[j], 2**j, 0) for j in range(3)])
        y_bv = Sum([If(y[j], 2**j, 0) for j in range(3)])
        return y_bv == (x_bv + 1) % 8
    
    def F(y):
        return And([y[j] == True for j in range(3)])
    
    return (I, T, F)

def FiniteRun(M, k):
    I, T, F = M
    solver = Solver()
    states = [[Bool(f'step_{i}_b{j}') for j in range(3)] for i in range(k + 1)]
    
    for j in range(3):
        solver.add(states[0][j] == I[j])
    
    for i in range(k):
        solver.add(T(states[i], states[i + 1]))
    
    solver.add(F(states[k]))
    
    if solver.check() == sat:
        print(f"FiniteRun (k={k}):  (Reaches 111)")
    else:
        print(f"FiniteRun (k={k}):  (Does not reach 111)")

def BMC(M, k):
    I, T, F = M
    solver = Solver()
    states = [[Bool(f'step_{i}_b{j}') for j in range(3)] for i in range(k + 1)]
    
    for j in range(3):
        solver.add(states[0][j] == I[j])
    
    for i in range(k):
        solver.add(T(states[i], states[i + 1]))
    
    solver.add(F(states[k]))
    
    if solver.check() == sat:
        print(f"BMC (k={k}):  (Reaches 111)")
    else:
        print(f"BMC (k={k}):  (Does not reach 111)")

def Interpolation(M, k):
    I, T, F = M
    solver = Solver()
    states = [[Bool(f'step_{i}_b{j}') for j in range(3)] for i in range(k + 1)]
    
    for j in range(3):
        solver.add(states[0][j] == I[j])
    
    for i in range(k):
        solver.add(T(states[i], states[i + 1]))
    
    solver.add(F(states[k]))
    
    if solver.check() == sat:
        print(f"Interpolation (k={k}):  (Reaches 111)")
    else:
        print(f"Interpolation (k={k}):  (Does not reach 111)")

def main():
    M = get_model_3bit()
    max_k = 9
    
    print("=== 3-Bit Binary Counter Verification ===")
    for k in range(1, max_k + 1):
        FiniteRun(M, k)
        BMC(M, k)
        Interpolation(M, k)
        print("---")

if __name__ == "__main__":
    main()
