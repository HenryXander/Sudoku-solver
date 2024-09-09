from collections import deque

def revise(csp, Xi, Xj):
    revised = False
    Di = csp.get_domain_from_var(Xi)
    Dj = csp.get_domain_from_var(Xj)
    constraint = csp.get_binary_constraint(Xi, Xj)
    for x in Di[:]:
        y_value = False
        for y in Dj:
            test_values = (x, y)
            if csp.satisfy_constraint(test_values, constraint):
                y_value = True
                break
        if not y_value:
            csp.delete_from_domain(Xi, x)
            revised = True
    return revised

def AC_3(csp): #Binary CSP with components X, D, C
    q = deque(csp.get_constraints().keys()) # fill queue with all arcs from csp
    while q:
        (Xi, Xj) = q.pop()
        if revise(csp, Xi, Xj):
            Di = csp.get_domain_from_var(Xi)
            if len(Di) == 0:
                return False
            for key in csp.get_constraints().keys():
                if key[1] == Xi:
                    Xk = key[0]
                    new_arc = (Xk, Xi)
                    q.append(new_arc)
    return True


def MAC(csp, var, assignment):
    q = deque()
    for neighbor in csp.neighbors[var]:
        if neighbor not in assignment:
            arc = (neighbor, var)
            q.append(arc)
    while q:
        (Xi, Xj) = q.pop()
        if revise(csp, Xi, Xj):
            Di = csp.get_domain_from_var(Xi)
            if len(Di) == 0:
                return False
            for key in csp.get_constraints().keys():
                if key[1] == Xi:
                    Xk = key[0]
                    new_arc = (Xk, Xi)
                    q.append(new_arc)
    return True