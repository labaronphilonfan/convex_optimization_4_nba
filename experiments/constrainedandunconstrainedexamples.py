##Taken from lecture notes 
# file:///C:/Users/henry/Downloads/ff36aa8c82776e1ac51115ea32d3a0f7_MIT6_079F09_lec04.pdf 
# for self referenece

#Constrained and unconstrained uptimization examples
#taken from pages:
#4 for definitions; dom(f0), gradf0(x) = 0, minimize f0(x) subj. to Ax = b.
#Requirements for optimal: x in dom(f0), Ax = b, *gradf0(x) + ATv = 0* WHY?????

#Standard minimization equality and inequality constraints equivalent to:
#**Minimize over z f0(Fz + x0) ...
#...
#...

#------------------------------------------------------------
#DIET PROBLEM
# ------------------------------------------------------------
#Goal:Find CHEAPEST diet meeting all nutritional requirements
#
# Setup:
#   -n foods to choose from
#   -x_j = quantity of food j we buy
#   - c_j = cost per unit of food j
#   - a_ij = amount of nutrient i in one unit of food j
#   - b_i = minimum required amount of nutrient i
#
# Formulation:
#   minimize    c^T x           (total cost)
#   subject to: Ax >= b         (meet all nutrient requirements)
#               x >= 0          (can't buy negative food)
#
#OUr frist example of Linear programming
#
# Example: 2 foods (chicken, beans), 2 nutrients (protein, fiber)
#   - chicken: $3/unit, 10g protein, 0g fiber
#   - beans:   $1/unit, 5g protein, 7g fiber
#   - need at least: 20g protein, 14g fiber




#EXAMPLE 1: Solve by hand (no imports) - 2 foods, 2 nutrients

#variables: x1 = chicken, x2 = beans
#
# Minimize: 3*x1 + 1*x2  (cost)
#Subject to:
#   10*x1 + 5*x2 >= 20   (protein)
#   0*x1 + 7*x2 >= 14    (fiber)
#   x1 >= 0, x2 >= 0
#
# WE want to olve by hand, and later use cxvpy for those with bigger maatrices
# From fiber:  7*x2 >= 14  -->  x2 >= 2
# Plug x2=2 into protein:  10*x1 + 10 >= 20  -->  x1 >= 1
# Optimal: x1=1, x2=2, Cost = 3*1 + 1*2 = $5

# Code it without imports (just basic Python)

# Step 1: Define the problem data clearly
CHICKEN_COST = 3      # $ per unit
BEANS_COST = 1        # $ per unit

CHICKEN_PROTEIN = 10  # grams per unit
BEANS_PROTEIN = 5     # grams per unit

CHICKEN_FIBER = 0     # grams per unit
BEANS_FIBER = 7       # grams per unit

MIN_PROTEIN = 20      # grams needed
MIN_FIBER = 14        # grams needed

# Step 2: Try all combinations and find the cheapest valid one
best_cost = float('inf')  # start with "infinity" (no solution yet)
best_chicken = 0
best_beans = 0

for chicken in range(0, 20):
    for beans in range(0, 20):

        #calculate nutrients from this combo
        total_protein = CHICKEN_PROTEIN * chicken + BEANS_PROTEIN * beans
        total_fiber = CHICKEN_FIBER * chicken + BEANS_FIBER * beans

        #Check if  this meet our requirement
        meets_protein = total_protein >= MIN_PROTEIN
        meets_fiber = total_fiber >= MIN_FIBER

        if meets_protein and meets_fiber:
            #Valid diet! so Calculate cost
            total_cost = CHICKEN_COST * chicken + BEANS_COST * beans

            # Is this cheaper than what we've found so far?
            if total_cost < best_cost:
                best_cost = total_cost
                best_chicken = chicken
                best_beans = beans

# Step 3: Print results
print(f"Best solution: {best_chicken} chicken, {best_beans} beans")
print(f"Total cost: ${best_cost}")

print('\n')
print('\n')
print('\n')
print('\n')


# EXAMPLE 2: Bigger problem - 5 foods, 4 nutrients (still by hand)

# Foods: chicken, beans, rice, eggs, milk
# Nutrients: protein, fiber, calcium, iron
#
# This is harder to solve by hand, but we can still brute force it!

def solve_diet_5_foods():
    """Solve a 5-food, 4-nutrient diet problem by  hand again"""

    #costs per unit: [chicken, beans, rice, eggs, milk]
    costs = [3, 1, 0.5, 2, 1.5]
    unit_name_keep_track = ['chicken', 'beans', 'rice', 'eggs', 'milk']
    #^placeholder variable for conveinece, not used in calculations

    # Nutrient matrix A (rows are nutrients, columns are foods)
    # Each row: how much of that nutrient is in each food
    #           chicken  beans  rice  eggs  milk
    A = [
        [10,      5,     2,    6,    3],    # protein (g)
        [0,       7,     1,    0,    0],    # fiber (g)
        [1,       4,     1,    5,    30],   # calcium (mg/10)
        [2,       2,     1,    3,    0],    # iron (mg)
    ]

    # Minimum requirements: [protein, fiber, calcium, iron]
    b = [25, 10, 50, 8]

    best_cost = float('inf')
    best_x = [0, 0, 0, 0, 0]

    # Brute force (limited range to keep it fast)
    #we are checking a cube of 8x8x8x8x8
    #our cube seach region is convex.
    # a hypercubne is convex
    #half spaces are x0 >=0 and x0 <= 8. Intersection of convex sets is convex.
    for x0 in range(0, 8):
        for x1 in range(0, 8):
            for x2 in range(0, 8):
                for x3 in range(0, 8):
                    for x4 in range(0, 8):
                        x = [x0, x1, x2, x3, x4]

                        #Check all of our nutrient constraints
                        feasible = True
                        for i in range(4):  # for each nutrient
                            nutrient_total = sum(A[i][j] * x[j] for j in range(5))
                            if nutrient_total < b[i]:
                                feasible = False
                                break

                        if feasible:
                            cost = sum(costs[j] * x[j] for j in range(5))
                            if cost < best_cost:
                                best_cost = cost
                                best_x = x[:]

    return best_x, best_cost

x, cost = solve_diet_5_foods()
print("EXAMPLE 2: 5 foods, 4 nutrients (brute force)")
print(f"  Foods [chicken, beans, rice, eggs, milk]: {x}")
print(f"  Total cost: ${cost}")
print()
print('\n')
print('\n')
print('\n')


# EXAMPLE 3: Large problem - 30 foods, 20 nutrients (need cvxpy!)
# Brute force is IMPOSSIBLE here: 10^30 combinations!
# This is why we need optimization libraries.
#
# With cvxpy, the LP solver uses smart math (simplex or interior point)
# to find the optimal solution efficiently.

import numpy as np
import cvxpy as cp

def solve_diet_large():
    """Solve a large diet problem using cvxpy"""

    np.random.seed(42)  # for reproducibility

    n_foods = 30
    n_nutrients = 20

    # Random costs between $0.50 and $5.00
    costs = np.random.uniform(0.5, 5.0, n_foods)

    # Random nutrient content matrix (how much of each nutrient in each food)
    A = np.random.uniform(0, 10, (n_nutrients, n_foods))

    # Random minimum requirements
    b = np.random.uniform(10, 30, n_nutrients)

    # Define the optimization variable
    x = cp.Variable(n_foods)

    # Objective: minimize cost
    objective = cp.Minimize(costs @ x)

    # Constraints: Ax >= b and x >= 0
    constraints = [
        A @ x >= b,
        x >= 0
    ]

    # Solve!
    problem = cp.Problem(objective, constraints)
    problem.solve()

    return x.value, problem.value, n_foods, n_nutrients

x, cost, n_foods, n_nutrients = solve_diet_large()
print(f"EXAMPLE 3: {n_foods} foods, {n_nutrients} nutrients (cvxpy)")
print(f"  Solution found! (showing first 5 foods)")
print(f"  Foods 0-4: {np.round(x[:5], 2)}")
print(f"  Total cost: ${cost:.2f}")
print()
print("Why cvxpy? Brute force would need to check ~10^30 combinations!")
print("cvxpy solves this in milliseconds using smart linear algebra.")


















# =============================================================================
# PIECEWISE-LINEAR MINIMIZATION
# =============================================================================
# Problem: minimize the MAX of several linear functions
#   minimize max_{i=1,...,m} (a_i^T x + b_i)
#
# Why is this tricky? The "max" function is not smooth/differentiable
#
# TRICK: Introduce a new variable t that upper-bounds all the linear functions
#   minimize t
#   subject to: a_i^T x + b_i <= t,  for i = 1,...,m
#
# Intuition:
#   - t must be >= all the (a_i^T x + b_i) values
#   - minimizing t pushes it down until it equals the largest one
#   - at optimum: t = max_i (a_i^T x + b_i)
#
# Variables: x (n-dimensional) and t (scalar)
# This is now a standard LP!