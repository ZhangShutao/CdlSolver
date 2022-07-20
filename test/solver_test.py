import unittest
import logging
from cdlsolver.preprocessor.preprocessor import Preprocessor
from cdlsolver.solver.solver import Solver
import clingo

logger = logging.getLogger()
logger.level = logging.DEBUG


class TestSolver(unittest.TestCase):

    def test_solve(self):
        program = 'fly(X) :- &c{fly(X)}, bird(X). bird(tweety).'
        ctl = clingo.Control(['0'])
        test_ctl = clingo.Control(['0'])
        defaults = set()
        preprocessor = Preprocessor(defaults, ctl, test_ctl)
        solver = Solver(ctl, test_ctl)

        preprocessor.preprocess(program)
        for model in solver.solve():
            print(model)

    def test_default_solve(self):
        program = 'p :- &c{s}. q :- &c{-s}.'
        ctl = clingo.Control(['0'])
        test_ctl = clingo.Control(['0'])
        defaults = set()
        preprocessor = Preprocessor(defaults, ctl, test_ctl)
        solver = Solver(ctl, test_ctl)

        preprocessor.preprocess(program)
        for model in solver.solve():
            print(model)
