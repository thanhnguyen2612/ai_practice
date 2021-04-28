def nullConstrants(problem, assignment):
    return False

class CSProblem:
    def __init__(self, variables=[], domains=[], constraintFunc=nullConstrants):
        self.variables = variables
        self.domains = domains
        self.constraintFunc = constraintFunc
    
    def isComplete(self, assignment):
        return len(assignment) == len(self.variables)
    
    def selectUnselectedVariable(self, assignment):
        for var in self.variables:
            if var not in assignment:
                return var
    
    def orderDomainValues(self, var, assignment):
        return [val for val in self.domains if self.isConsistent(var, val, assignment)]
    
    def isConsistent(self, var, val, assignment):
        temp = assignment.copy()
        temp[var] = val
        return self.constraintFunc(self, temp)


def cryptharithmeticConstraints(problem, assignment):
    """
    @Return:
        True: if satisfy constraints
    """
    unique = set()
    for var, val in assignment.items():
        if var in ['X1', 'X2', 'X3']:
            continue
        if val in unique:
            return False
        else:
            unique.add(val)
    if 'T' in assignment and assignment['T'] == 0:
        return False
    if 'F' in assignment and assignment['F'] == 0:
        return False
    if 'O' in assignment and 'R' in assignment and 'X1' in assignment and\
        assignment['O'] * 2 != assignment['R'] + 10 * assignment['X1']:
        return False
    if 'W' in assignment and 'U' in assignment and\
        'X1' in assignment and 'X2' in assignment and\
        assignment['W'] * 2 + assignment['X1'] != assignment['U'] + 10 * assignment['X2']:
        return False
    if 'T' in assignment and 'O' in assignment and\
        'X2' in assignment and 'X3' in assignment and\
        assignment['T'] * 2 + assignment['X2'] != assignment['O'] + 10 * assignment['X3']:
        return False
    if 'F' in assignment and 'X3' in assignment and assignment['F'] != assignment['X3']:
        return False
    return True
    

def backtracking_search(csp, assignment={}):
    return recursive_backtracking(assignment, csp)

def recursive_backtracking(assignment, csp):
    if csp.isComplete(assignment):
        return assignment
    
    var = csp.selectUnselectedVariable(assignment)
    for val in csp.orderDomainValues(var, assignment):
        assignment[var] = val
        result = recursive_backtracking(assignment, csp)
        if result:
            return result
        del assignment[var]

    return {}

if __name__ == "__main__":
    variables = ['T', 'W', 'O', 'F', 'U', 'R', 'X1', 'X2', 'X3']
    domains = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    cryptharithmetic = CSProblem(variables, domains, cryptharithmeticConstraints)

    result = backtracking_search(cryptharithmetic)
    print(result)