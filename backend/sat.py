import random
from pysat.solvers import Solver


class Sat:
    @staticmethod
    def generate_problem(num_vars: int = 3, num_clauses: int = 10) -> str:
        """
        Generates and returns a SAT problem in kCNF form, where k=self.num_vars
        Parameters:
            num_vars: number of unique variables
            num_clauses: number of kCNF clauses
        Returns:
            str: a string representation of 2D kCNF clauses, with each clause
                separated by a '&' and each literal separated by a '|'.
                Each literal in the clause is in the range [-k, -1] U [1, k],
                the negative sign represents the negation of the variable
        """
        candidate_vars = [i for i in range(1, num_vars + 1)]
        clauses = []

        # builds up each clause
        for i in range(num_clauses):
            random.shuffle(candidate_vars)
            curr_clause = []

            # builds up each variable in current clause
            for j in range(num_vars):
                is_negated = random.choice([-1, 1])
                curr_var = candidate_vars[j]
                curr_clause.append(is_negated * curr_var)

            clauses.append(curr_clause)

        # converts the list of kCNF clauses to str
        return '&'.join(
            ['|'.join(
                [str(literal) for literal in clause]
            ) for clause in clauses]
        )

    @staticmethod
    def solve(problem: str) -> str:
        """
        Attempts to solve the SAT problem
        Parameters:
            problem: the string representation of multiple kCNF clauses, in the
                form generated by self.generate_problem()
        Returns:
            str: a string representation of the variable assignment joined by
                ',', or empty string if the problem is not solvable
        """
        # parses the string into a 2D list
        clauses = [
            [int(literal) for literal in clause.split('|')]
            for clause in problem.split('&')
        ]
        s = Solver(bootstrap_with=clauses)

        if s.solve():  # if the problem is solved
            return ','.join([str(literal) for literal in s.get_model()])
        else:
            return ''

    @staticmethod
    def verify(problem: str, answer: str) -> bool:
        """
        Verifies the answer to the SAT problem. Parameter formats are
        defined in self.solve() and self.generate_problem().
        """
        # parses the problem into a 2D list
        clauses = [clause.split('|') for clause in problem.split('&')]
        # parses the answer into a set
        assignments = {literal for literal in answer.split(',')}

        for clause in clauses:
            intersection = set(clause).intersection(assignments)
            if len(intersection) == 0:
                # none of the literals in current clause is evaluated to True
                # the assignment failed
                return False

        return True  # none of the clauses is False, the assignment is verified