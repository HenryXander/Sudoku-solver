from collections import deque

def PC_2(csp):
    q = deque(csp.get_constraints().keys())
    while q:
        (Xi, Xj) = q.popleft()
        if revise(csp, Xi, Xj):
            for Xk in csp.neighbors[Xi]:
                if Xk != Xj:
                    q.append((Xk, Xi))
    return True



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