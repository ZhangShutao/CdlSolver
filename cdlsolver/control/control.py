import logging
from abc import ABC
import clingo
from cdlsolver.preprocessor.preprocessor import Preprocessor
# from cdlsolver.postprocessor.postprocessor import Postprocessor
from cdlsolver.solver.solver import Solver, DefaultModel


def silent_logger(_code, _msg):
    pass


class Control(ABC):

    def __init__(self):
        self._rules = []
        self._defaults = set()
        self._candidate_ctl = clingo.Control(['0'], logger=silent_logger)
        self._shows = []

    def add(self, program):
        """
        Add a sub-program to the control.

        :param program: the string of new sub-program
        :return: 0 if success
        """
        # self._program = self._program + program
        preprocessor = Preprocessor(self._defaults, self._candidate_ctl, self._rules, self._shows)
        preprocessor.preprocess(program)
        return 0

    def load(self, input_path):
        """
        Load a program file from specific path.

        :param input_path: the absolute path of the input program file
        :return: 0 if success, 1 if failed
        """
        with open(input_path, 'r') as program_file:
            return self.add(program_file.read())
    #
    # def parse(self):
    #     """
    #
    #     :return:
    #     """
    #     return 0

    def solve(self):
        """
        Solve the loaded program.

        :return: models, the list is empty if the program is unsatisfiable
        """
        # logging.debug('solving asp program:' + '\n'.join(self._rules))
        solver = Solver(self._candidate_ctl, self._defaults, self._rules, self._shows)
        # with  as models:
        models = solver.solve()

        del solver
        return models
