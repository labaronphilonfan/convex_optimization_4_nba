#First file in project, aimed at
#doing basic math operations to learn from scratch


#Optimizing convex quadratic in 2D
#Steps:
#1) Compute Aw (matrix times vector)
#2) Compute wT(Aw) (dot product)
#3) Multiply by 0.5
#4) Compute bTw (dot product)
#5) Subtract step 4 from step 3


import numpy as np

#Matrix A
A = np.array([[3,1], [1,2]])

#Vector b
b = np.array([1,1])

#w is point we want to evaluate
w = np.array([1,1])

#Step 1:
Aw = np.dot(A, w)
print("STEP 1: Aw  = ", Aw)
print("\n")

#Step 2:
wTAw = np.dot(w, Aw)
print("STEP 2: wT * Aw  = ", wTAw)
print("\n")

#Step 3:
half_wTAw = 0.5 * wTAw
print("STEP 3: 0.5 * wT * Aw  = ", half_wTAw)
print("\n")

#Step 4:
bTw = np.dot(b, w)
print("STEP 4: bT * w  = ", bTw)
print("\n")

#Step 5:
objective_value = half_wTAw - bTw
print("STEP 5: Objective Value  = ", objective_value)
print("\n")



