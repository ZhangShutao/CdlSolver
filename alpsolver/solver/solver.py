import logging
from abc import ABC
import clingo.ast
import clingo.symbol
import re


def silent_logger(_code, _msg):
    pass


class DefaultModel:

    def __init__(self, symbols, x=None, y=None, guess=None):
        self._symbols = symbols
        if x is None:
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
                        self._y.add(DefaultModel.get_symbol_from_guess(symbol))
        else:
            self._x = x
            self._y = y
            self._guess = guess

        self._assumption = set()
        for g in self._guess:
            (atom, neg) = (DefaultModel.get_symbol_from_guess(g), 'guess_not_' in g.name)
            self._assumption.add((atom, neg))

    def symbols(self):
        return self._symbols

    def x(self):
        return self._x

    def assumption(self):
        return self._assumption

    def count_guess(self):
        return len(self._guess)

    def covers(self, other):
        if not isinstance(other, DefaultModel):
            return False

        for g in other._guess:
            if g not in self._guess:
                return False
        return len(self._guess) > len(other._guess)

    @staticmethod
    def get_symbol_from_guess(symbol):
        if 'guess_' not in symbol.name:
            return None

        sneg = 'sn_' in symbol.name

        guess_regex = re.compile(r"guess_(not_)?(sn_)?")
        literal_name = guess_regex.sub("", symbol.name)
        return clingo.symbol.Function(literal_name, symbol.arguments, not sneg)

    def filter_shows(self, shows):
        if len(shows) > 0:
            show_list = []
            guess_show = []
            for s in shows:
                show_list.append((s.positive, s.name, s.arity))
                guess_show.append((True, ('guess_' if s.positive else 'guess_sn_') + s.name, s.arity))
                guess_show.append((True, ('guess_not_' if s.positive else 'guess_not_sn_') + s.name, s.arity))

            # print(guess_show)
            new_x = set(filter(lambda x: (x.positive, x.name, len(x.arguments)) in show_list, self._x))
            new_y = set(filter(lambda y: (y.positive, y.name, len(y.arguments)) in show_list, self._y))
            new_guess = set(filter(lambda g: (g.positive, g.name, len(g.arguments)) in guess_show, self._guess))
            return DefaultModel(self._symbols, new_x, new_y, new_guess)
        else:
            return DefaultModel(self._symbols, self._x, self._y, self._guess)

    def __key(self):
        return ';'.join([str(g) for g in self._guess])

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, DefaultModel):
            return self.__key() == other.__key()
        return NotImplemented

    def __repr__(self):
        return 'X:' + ', '.join([str(m) for m in self._x]) + ';\n' \
               'A:' + ', '.join([('not ' if neg else '') + str(a) for (a, neg) in self._assumption]) + ';'


class Solver(ABC):

    def __init__(self, candidate_ctl, defaults, rules, shows):
        self._models = []
        self._candidate_ctl = candidate_ctl
        self._candidates = []
        self._defaults = defaults
        self._rules = rules
        self._shows = shows

    def solve(self):
        # print('\n'.join(self._rules))
        try:
            self._candidate_ctl.ground([('base', [])])
            logging.debug('program grounded')
        except RuntimeError as e:
            raise
        with self._candidate_ctl.solve(yield_=True) as handle:
            logging.debug('asp program solving')
            for model in handle:
                answer_set = model.symbols(shown=True)
                self._candidates.append(DefaultModel(answer_set))
            logging.debug('asp solved with %d models', len(self._candidates))

        self._candidates = sorted(self._candidates, key=DefaultModel.count_guess, reverse=True)

        for i in range(len(self._candidates)):
            # logging.debug("candidate:{0}".format(self._candidates[i]))
            if not self._candidate_covered(self._candidates[i]) and self._test_Y_part(self._candidates[i].symbols()):
                self._models.append(self._candidates[i])

        return self._models

    def _test_Y_part(self, answer_set):
        # logging.debug('y testing...')
        test_rules = self._rules.copy()
        assumptions = [(symbol, True) for symbol in answer_set]
        guesses = list(filter(lambda symbol: 'guess_' in symbol.name, answer_set))

        for symbol in guesses:
            objective = DefaultModel.get_symbol_from_guess(symbol)
            naf = 'guess_not_' in symbol.name
            # print("external:" + str(objective) + ":" + str(not naf))
            assumptions.append((objective, not naf))

        for assume, truth in assumptions:
            if truth:
                test_rules.append(str(assume) + ".")
            else:
                test_rules.append("not " + str(assume) + ".")
        # logging.debug('\n'.join(test_rules))
        print(test_rules)

        ctl = clingo.Control(['0'], logger=silent_logger)
        ctl.add('base', [], '\n'.join(test_rules))

        ctl.ground([('base', [])])
        with ctl.solve(yield_=True) as result_handle:
            m = result_handle.model()
            if m is None:
                return False
            else:
                return True
            # print('y test:' + str(ret))
        #
        # for symbol in guesses:
        #     objective = DefaultModel.get_symbol_from_guess(symbol)
        #     print("releasing external :" + str(objective))
        #     self._test_ctl.release_external(objective)

    def _candidate_covered(self, candidate_model):
        for dm in self._models:
            if dm.covers(candidate_model):
                # print(str(dm) + ' covers ' + str(candidate_model))
                return True
            # else:
            #     print(str(candidate_model) + ' covers ' + str(dm))
        return False

    def shows(self):
        return self._shows
