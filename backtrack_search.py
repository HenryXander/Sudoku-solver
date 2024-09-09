from copy import deepcopy
from AC3 import AC_3, MAC
from PC2 import PC_2
from forward_checking import forward_checking

def select_unassigned_variable(csp, assignment):
    unassigned_variables = [var for var in csp.X if var not in assignment]
    # Sort the unassigned variables based on the number of remaining values in their domain
    sorted_variables = sorted(unassigned_variables, key=lambda var: len(csp.get_domain_from_var(var)))
    return sorted_variables[0] if sorted_variables else None

def order_domain_values(var, assignment, csp):
    domain = csp.get_domain_from_var(var)
    # Sort the values in the domain based on the number of constraints they rule out in other variables
    sorted_values = sorted(domain, key=lambda value: count_constraints_ruled_out(var, value, assignment, csp))
    return sorted_values

def count_constraints_ruled_out(var, value, assignment, csp):
    count = 0
    # Assign the value to the variable temporarily
    assignment[var] = value
    # Check each unassigned variable to see how many values would be ruled out by this assignment
    for unassigned_var in [v for v in csp.X if v not in assignment and v != var]:
        unassigned_domain = csp.get_domain_from_var(unassigned_var)
        # Count the number of values ruled out by the assignment
        for unassigned_value in unassigned_domain:
            test_values = (value, unassigned_value)
            if not csp.satisfy_constraint(test_values, csp.get_binary_constraint(var, unassigned_var)):
                count += 1
    # Remove the temporary assignment
    del assignment[var]
    return count

def inference(csp, var, value, assignment, inference_type):
    csp_copy = deepcopy(csp)
    if inference_type == "forward_checking":
        forward_checking_result = forward_checking(csp_copy, var, value, assignment)
        return (forward_checking_result, csp_copy)
    elif inference_type == "ac3":
        ac_3_result = AC_3(csp_copy)
        return (ac_3_result, csp_copy)
    elif inference_type == "pc2":
        pc_2_result = PC_2(csp_copy)
        return (pc_2_result, csp_copy)
    elif inference_type == "mac":
        mac_result = MAC(csp_copy, var, assignment)
        return (mac_result, csp_copy)
    else:
        raise ValueError("Invalid inference type")

def consistent_test(csp, subassignment, assignment):
        assignment = assignment | subassignment
        for (var1, var2), constraint in csp.C.items():
            if var1 in assignment and var2 in assignment:
                values = (assignment[var1], assignment[var2])
                if not constraint(values):
                    return False
        return True

def backtrack(assignment, csp, inference_type):
    if csp.assignment_complete(assignment):
        return assignment
    var = select_unassigned_variable(csp, assignment)
    for value in order_domain_values(var, assignment, csp):
        subassignment = {var : value}
        if consistent_test(csp, subassignment, assignment):
            assignment = assignment | subassignment
            inferences = inference(csp, var, value, assignment, inference_type) #return (status, csp) with status being true or false and csp a CSP class object
            result = inferences[0]
            new_csp = inferences[1]
            if result:
                result = backtrack(assignment, new_csp, inference_type)
                if result != "Failure":
                    return result
        if var in assignment:
            del assignment[var]
    return "Failure"

def backtracking_search_CSP(csp, inference_type):
    return backtrack({}, csp, inference_type)