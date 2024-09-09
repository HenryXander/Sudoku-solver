def forward_checking(csp, var, value, assignment):
    for neighbor in csp.neighbors[var]:
        if neighbor not in assignment:
            binary_constraint = csp.get_binary_constraint(var, neighbor)
            if binary_constraint:
                remaining_values = []
                for neighbor_value in csp.get_domain_from_var(neighbor):
                    values = (value, neighbor_value)
                    if csp.satisfy_constraint(values, binary_constraint):
                        remaining_values.append(neighbor_value)
                if not remaining_values:
                    return False
                csp.set_domain_from_var(neighbor, remaining_values)
    return True