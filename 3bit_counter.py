from z3 import *

# === 3-Bit Counter Model ===
def get_model_3bit():
    I = [False, False, False]  # Initial state (000)
    
    def T(x, y):
        """Transition: x → y (increment by 1, mod 8)."""
        x_bv = Sum([If(x[j], 2**j, 0) for j in range(3)])
        y_bv = Sum([If(y[j], 2**j, 0) for j in range(3)])
        return y_bv == (x_bv + 1) % 8
    
    def F(y):
        """Final state: 111 (binary 7)."""
        return And([y[j] == True for j in range(3)])
    
    return (I, T, F)

# === Finite Run Verification ===
def FiniteRun(M, k):
    I, T, F = M
    solver = Solver()
    states = [[Bool(f'step_{i}_b{j}') for j in range(3)] for i in range(k + 1)]
    
    # Initial state
    for j in range(3):
        solver.add(states[0][j] == I[j])
    
    # Transitions
    for i in range(k):
        solver.add(T(states[i], states[i + 1]))
    
    # Final state check
    solver.add(F(states[k]))
    
    if solver.check() == sat:
        print(f"FiniteRun (k={k}):  (Reaches 111)")
    else:
        print(f"FiniteRun (k={k}):  (Does not reach 111)")

# === Bounded Model Checking (BMC) ===
def BMC(M, k):
    I, T, F = M
    solver = Solver()
    states = [[Bool(f'step_{i}_b{j}') for j in range(3)] for i in range(k + 1)]
    
    # Initial state
    for j in range(3):
        solver.add(states[0][j] == I[j])
    
    # Transitions
    for i in range(k):
        solver.add(T(states[i], states[i + 1]))
    
    # Final state check
    solver.add(F(states[k]))
    
    if solver.check() == sat:
        print(f"BMC (k={k}):  (Reaches 111)")
    else:
        print(f"BMC (k={k}):  (Does not reach 111)")

# === Interpolation-Based Verification ===
def Interpolation(M, k):
    I, T, F = M
    solver = Solver()
    states = [[Bool(f'step_{i}_b{j}') for j in range(3)] for i in range(k + 1)]
    
    # Initial state
    for j in range(3):
        solver.add(states[0][j] == I[j])
    
    # Transitions
    for i in range(k):
        solver.add(T(states[i], states[i + 1]))
    
    # Final state check
    solver.add(F(states[k]))
    
    if solver.check() == sat:
        print(f"Interpolation (k={k}):  (Reaches 111)")
    else:
        print(f"Interpolation (k={k}):  (Does not reach 111)")

# === Run All Methods ===
def main():
    M = get_model_3bit()
    max_k = 9  # Test up to k=9 (000 → 001 → ... → 111 → 000 → ...)
    
    print("=== 3-Bit Binary Counter Verification ===")
    for k in range(1, max_k + 1):
        FiniteRun(M, k)
        BMC(M, k)
        Interpolation(M, k)
        print("---")

if __name__ == "__main__":
    main()