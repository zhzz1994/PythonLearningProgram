from pulp import *

cost = LpProblem('money',LpMinimize)
x1 = LpVariable('x1', lowBound = 0)
x2 = LpVariable('x2', lowBound = 0)
x3 = LpVariable('x3', lowBound = 0)
x4 = LpVariable('x4', lowBound = 0)

cost += x1 + x2 + x3 + x4
cost += -2*x1 + 8*x2 + 0*x3 + 10*x4 >= 50
cost += 5*x1 + 2*x2 + 0*x3 + 0*x4 >= 100
cost += 3*x1 - 5*x2 + 10*x3 - 2*x4 >= 25

cost.solve()
for i in cost.variables():
    print(value(cost.objective))