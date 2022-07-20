from abc import ABC
import clingo.ast
import clingo.symbol
import re


class DefaultModel:

    def __init__(self, symbols):
        self._symbols = symbols
        self._x = set()
        self._y = set()
        self._guess = set()
        for symbol in symbols:
            if 'guess_' not in symbol.name:
                self._x.add(symbol)
                self._y.add(symbol)
            else:
                self._guess.add(symbol)
                if 'guess_not_' not in symbol.name:
                    self._y.add(DefaultModel.get_objective_literal_from_guess(symbol))

    def count_guess(self):
        return len(self._guess)

    def covers(self, other):
        for g in other._guess:
            if g not in self._guess:
                return False
        return True

    @staticmethod
    def get_objective_literal_from_guess(symbol):
        positive = True
        if 'guess_' not in symbol.name or 'not_' in str(symbol.name):
            return None
        if 'sn_' in str(symbol.name):
            positive = False

        guess_regex = re.compile(r"(guess_)|(not_)|(sn_)")
        literal_name = guess_regex.sub("", symbol.name)
        return clingo.symbol.Function(literal_name, symbol.arguments, positive)

    def __key(self):
        return ';'.join([str(g) for g in self._guess])

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, DefaultModel):
            return self.__key() == other.__key()
        return NotImplemented

    def __repr__(self):
        return 'x:' + ','.join([str(m) for m in self._x]) + '; y:' + ','.join([str(m) for m in self._y]) + ';'


class Solver(ABC):

    def __init__(self, candidate_ctl, test_ctl):
        self._models = []
        self._candidate_ctl = candidate_ctl
        self._test_ctl = test_ctl
        self._candidates = []

    def solve(self):
        self._candidate_ctl.ground([('base', [])])
        with self._candidate_ctl.solve(yield_=True) as handle:
            for model in handle:
                # print(model)
                answer_set = model.symbols(shown=True)
                if self._test_Y_part(answer_set):
                    self._candidates.append(DefaultModel(answer_set))

        self._candidates = sorted(self._candidates, key=DefaultModel.count_guess, reverse=True)

        for i in range(len(self._candidates)):
            if not self._candidate_covered(self._candidates[i]):
                self._models.append(self._candidates[i])

        return self._models

    def _test_Y_part(self, answer_set):
        assumptions = [(symbol, True) for symbol in answer_set]

        for symbol in answer_set:
            objective = DefaultModel.get_objective_literal_from_guess(symbol)
            if objective is not None:
                assumptions.append((objective, True))

        with self._test_ctl.solve(yield_=True, assumptions=assumptions) as result_handle:
            # print(result_handle.get())
            return result_handle.get().satisfiable

    def _candidate_covered(self, candidate_model):
        for dm in self._models:
            if dm.covers(candidate_model):
                # print(str(dm) + ' covers ' + str(candidate_model))
                return True
            # else:
            #     print(str(candidate_model) + ' covers ' + str(dm))
        return False
