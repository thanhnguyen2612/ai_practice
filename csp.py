import random

class CSP:
    def __init__(self, variables, domains, neighbors, constraints):
        variables = variables or list(domains.key())
        self.variables = variables
        self.domains = domains
        self.neighbors = neighbors
        self.constraints = constraints
        self.curr_domains = domains.copy()
        self.nassigns = 0
    
    def assign(self, var, val, assignment):
        assignment[var] = val
        self.nassigns += 1
    
    def unassign(self, var, assignment):
        if var in assignment:
            del assignment[var]
    
    def nconflicts(self, var, val, assignment):
        def conflict(var2):
            return var2 in assignment and not self.constraints(var, val, var2, assignment[var2])

        return sum(conflict(v) for v in self.neighbors[var])
    
    def support(self, var, val):
        removals = [(var, a) for a in self.curr_domains[var] if a != val]
        self.curr_domains[var] = [val]
        return removals
    
    def restore(self, removals):
        for var, val in removals:
            self.curr_domains[var].append(val)
    
    def prune(self, var, val, removals):
        self.curr_domains[var].remove(val)
        if removals is not None:
            removals.append((var, val))

    # Graph search interface
    def expand(self, state):
        if len(state) == len(self.variables):
            return []
        else:
            assignment = dict(state)
            var = [v for v in self.variables if v not in assignment][0]
            return [(var, val) for val in self.domains[var]
                    if self.nconflicts(var, val, assignment) == 0]

    def getNextState(self, state, action):
        (var, val) = action
        return state + ((var, val),)
    
    def isGoalState(self, state):
        assignment = dict(state)
        return (len(assignment) == len(self.variables)
                and all(self.nconflicts(var, assignment[var], assignment) == 0
                        for var in self.variables))

def AC3(csp):
    queue = {(Xi, Xj) for Xi in csp.variables for Xj in csp.neighbors[Xi]}

    while queue:
        (Xi, Xj) = queue.pop()
        if remove_inconsistent_values(csp, Xi, Xj):
            if not csp.curr_domains[Xi]:
                return False
            for Xk in csp.neighbors[Xi]:
                if Xk != Xj:
                    queue.add((Xk, Xi))
    return True

def remove_inconsistent_values(csp, Xi, Xj):
    removed = False
    for x in csp.curr_domains[Xi]:
        if any(csp.constraints(Xi, x, Xj, y) for y in csp.curr_domains[Xj]):
            continue
        else:
            csp.curr_domains[Xi].remove(x)
            removed = True
    return removed

def forward_checking(csp, var, val, assignment, removals):
    """Prune neighbor values inconsistent with var=value."""
    for neighbor in csp.neighbors[var]:
        if neighbor not in assignment:
            for neighbor_val in csp.curr_domains[neighbor][:]:
                if not csp.constraints(var, val, neighbor, neighbor_val):
                    csp.prune(neighbor, neighbor_val, removals)
            if not csp.curr_domains[neighbor]:
                return False
    return True

def first_unassigned_variable(assignment, csp):
    return [var for var in csp.variables if var not in assignment][0]

def lcv(var, assignment, csp):
    return sorted(csp.curr_domains[var], key=lambda val: csp.nconflicts(var, val, assignment))

##################################### Search algorithm #####################################

def backtracking_search(csp, select_unassigned_variable=first_unassigned_variable,
                        order_domain_values=lcv, inferences=forward_checking, assignment={}):
    AC3(csp)
    def recursive_backtracking(assignment={}):
        if len(assignment) == len(csp.variables):
            return assignment

        var = select_unassigned_variable(assignment, csp)
        for val in order_domain_values(var, assignment, csp):
            if csp.nconflicts(var, val, assignment) == 0:
                csp.assign(var, val, assignment)

                # Make inference
                removals = csp.support(var, val)
                if inferences(csp, var, val, assignment, removals):
                    result = recursive_backtracking(assignment)
                    if result:
                        return result
                # Remove inference
                csp.restore(removals)
                csp.unassign(var, assignment)
        return {}
    return recursive_backtracking(assignment)

def min_conflicts(csp, max_steps=100):
    assignment = {var: csp.curr_domains[var][0] for var in csp.variables}
    for i in range(max_steps):
        if csp.isGoalState(assignment):
            return assignment
        conflict_vars = [var for var in assignment 
                                if csp.nconflicts(var, assignment[var], assignment) > 0]
        var = random.choice(conflict_vars)
        val = sorted(csp.curr_domains[var], key=lambda val: csp.nconflicts(var, val, assignment))[0]
        csp.assign(var, val, assignment)
    
    return {}