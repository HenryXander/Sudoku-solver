class CSP: #Binaire CSP
    def __init__(self, X, D, C):
        self.X = X
        self.D = D #D is a dict, with Xi as key and domain list as value
        self.C = C #C is a dict, with (Xi, Xj) as key and the constraint function as value

        self.neighbors = self.__initialize_neighbors()


    def __initialize_neighbors(self):
        neighbors = {var: [] for var in self.X}
        for (var1, var2) in self.C:
            neighbors[var1].append(var2)
            neighbors[var2].append(var1)
        return neighbors


    def get_neighbors(self, var):
        return self.neighbors[var]

    def get_domain_from_var(self, Xi):
        if Xi in self.D:
            return self.D[Xi]
        return None

    def set_domain_from_var(self, Xi, domain):
        self.D[Xi] = domain

    def delete_from_domain(self, Xi, x):
        if Xi in self.D:
            if x in self.D[Xi]:
                self.D[Xi].remove(x)

    def get_binary_constraint(self, Xi, Xj):
        if (Xi, Xj) in self.C:
            return self.C[(Xi, Xj)]
        return None

    def satisfy_constraint(self, values, constraint):
        if constraint is None:
            return True
        return constraint(values)

    def get_constraints(self):
        return self.C

    def assignment_complete(self, assignment):
        if len(self.X) == len(assignment.keys()):
            return True
        return False

    def consistent_test(self, subassignment, assignment):
        assignment = assignment | subassignment
        for (var1, var2), constraint in self.C.items():
            if var1 in assignment and var2 in assignment:
                values = (assignment[var1], assignment[var2])
                if not constraint(values):
                    return False
        return True

    def valid(self, assignment):
        for (var1, var2), constraint in self.C.items():
            if var1 in assignment and var2 in assignment:
                values = (assignment[var1], assignment[var2])
                if not constraint(var1, var2, values[0], values[1]):
                    return False
        return True

    def toString(self):
        string = " variables : {}\n domains : {}\n constraints : {}\n".format(self.X, self.D, self.C)
        return string