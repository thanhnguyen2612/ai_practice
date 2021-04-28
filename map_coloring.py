import csp

# Lists of states
variables = ["WA", "NT", "SA", "Q", "NSW", "V", "T", ]

# Domains
domains = {var: ["red", "green", "blue"] for var in variables}

# Neighbors
neighbors = {
    "WA": ["SA", "NT"],
    "NT": ["WA", "SA", "Q"],
    "SA": ["WA", "NT", "Q", "NSW", "V"],
    "Q": ["NT", "SA", "NSW"],
    "NSW": ["Q", "SA", "V"],
    "V": ["SA", "NSW"],
    "T": []
}

def constraintFunc(var1, val1, var2, val2):
    return var2 not in neighbors[var1] or val1 != val2

problem = csp.CSP(variables, domains, neighbors, constraintFunc)

# print(csp.backtracking_search(problem))
print(csp.min_conflicts(problem, 100000))