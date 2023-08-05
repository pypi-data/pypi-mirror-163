from time import time

from scipy import optimize as scipy_optimize
import numpy as np

from flopt.solvers.base import BaseSearch
from flopt.solvers.solver_utils import (
    during_solver_message,
    end_solver_message
)
from flopt.convert import LpStructure
from flopt.env import setup_logger
from flopt.expression import Const
from flopt.solution import Solution
from flopt.constants import VariableType, SolverTerminateState


logger = setup_logger(__name__)


class ScipyMilpSearch(BaseSearch):
    """Scipy optimize milp API Solver

    Note
    ----
    In scipy version 1.9.0,
    we can not obtain the incumbent solution from scipy.optimize.milp API,
    and can not use callback to this API for logging.
    Therefore, we can obtain the solution when only scipy.optimize.milp terminate the execution normally.

    See Also
    --------
    scipy.optimize.milp

    Returns
    -------
    status : int
        status of solver
    """
    def __init__(self):
        super().__init__()
        self.name = "ScipyMilpSearch"
        self.can_solve_problems = ['mip']


    def available(self, prob, verbose=False):
        """
        Parameters
        ----------
        prob : Problem
        verbose : bool

        Returns
        -------
        bool
            return true if it can solve the problem else false
        """
        for var in prob.getVariables():
            if not var.type() in {VariableType.Continuous, VariableType.Binary, VariableType.Integer}:
                logger.error(f"variable: \n{var}\n must be continouse, binary or interger, but got {var.type()}")
                return False
        if not prob.obj.isLinear():
            logger.error(f"objective function: \n{prob.obj}\n must be Linear")
            return False
        for const in prob.constraints:
            if not const.expression.isLinear():
                logger.error(f"constraint: \n{const}\n must be Linear")
                return False
        return True


    def search(self):
        status = SolverTerminateState.Normal
        var_names = [var.name for var in self.solution]

        def gen_func(expression):
            def func(values):
                variables = []
                for var_name, value in zip(var_names, values):
                    variables.append(Const(value, name=var_name))
                solution = Solution('tmp', variables)
                return expression.value(solution)
            return func

        # function
        func = gen_func(self.prob.obj)

        # lp structure
        lp = LpStructure.fromFlopt(self.prob, x=self.solution.getVariables()).toAllNeq()

        # bounds
        lbs = [_lb if not np.isnan(_lb) else -np.inf for _lb in lp.lb]
        ubs = [_ub if not np.isnan(_ub) else np.inf  for _ub in lp.ub]
        bounds = scipy_optimize.Bounds(lbs, ubs)

        # integrality
        integrality = [False if var.type() == VariableType.Continuous else True for var in lp.x]

        # constraints (lp.G x <= lp.h)
        no_constraints = lp.G is None
        if not no_constraints:
            constraints = scipy_optimize.LinearConstraint(lp.G, np.full_like(lp.h, -np.inf), lp.h)
        else:
            constraints = None

        # options
        options = {'disp': self.msg, 'time_limit': self.timelimit}

        # search
        res = scipy_optimize.milp(
            c=lp.c,
            constraints=constraints,
            integrality=integrality,
            bounds=bounds,
            options=options,
            )
        # res.status =  0: Optimal solution found.
        #               1: Iteration or time limit reached.
        #               2: Problem is infeasible.
        #               3: Problem is unbounded.
        #               4: Other; see message for details.
        if res.status == 0:
            # get result of solver
            for var, value in zip(self.solution, res.x):
                var.setValue(value)
            self.updateSolution(self.solution, obj_value=None)
        elif res.status == 1:
            status = SolverTerminateState.Timelimit
        elif res.status == 2:
            status = SolverTerminateState.Infeasible
        elif res.status == 3:
            status = SolverTerminateState.Unbounded
        else:
            status = SolverTerminateState.Abnormal

        return status

