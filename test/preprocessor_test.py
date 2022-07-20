import unittest
from cdlsolver.preprocessor.preprocessor import Preprocessor
import clingo.ast
import logging


logger = logging.getLogger()
logger.level = logging.DEBUG


class VisitTransformer(clingo.ast.Transformer):

    def visit_Literal(self, literal):
        print(literal)
        print(literal.atom.symbol)
        return literal


class TestPreprocessor(unittest.TestCase):

    def test_guess_literals(self):
        defaults = set()
        candidate_ctl = clingo.Control(['0'])
        test_ctl = clingo.Control(['0'])
        preprocessor = Preprocessor(defaults, candidate_ctl, test_ctl)
        program = 'a :- &c{not b}. b:- not &c{-a}.'
        # clingo.ast.parse_string('a :-guess_not_b. b:- not guess_not_sn_a.', vtm)
        preprocessor.preprocess(program)

        targets = ['guess_sn_a', 'guess_not_b']
        for target in targets:
            self.assertIn(target, [str(default) for default in defaults])

    def test_guess_literals_with_arg(self):
        defaults = set()
        candidate_ctl = clingo.Control(['0'])
        test_ctl = clingo.Control(['0'])
        preprocessor = Preprocessor(defaults, candidate_ctl, test_ctl)
        program = 'a(X) :- &c{not -b(f(X))}, c(X).'
        preprocessor.preprocess(program)
        for rule in preprocessor._additional_rules:
            print(rule)

        targets = ['guess_not_sn_b(f(X))']
        for target in targets:
            self.assertIn(target, [str(default) for default in defaults])

    def test_choose_rule_construct(self):
        defaults = set()
        candidate_ctl = clingo.Control(['0'])
        test_ctl = clingo.Control(['0'])
        preprocessor = Preprocessor(defaults, candidate_ctl, test_ctl)
        program = 'fly(X) :- &c{fly(X)}, bird(X). bird(tweety).'
        preprocessor.preprocess(program)
        for rule in preprocessor._additional_rules:
            print(rule)

    def test_guess_literal(self):
        defaults = set()
        candidate_ctl = clingo.Control(['0'])
        test_ctl = clingo.Control(['0'])
        preprocessor = Preprocessor(defaults, candidate_ctl, test_ctl)
        program = 'fly(X) :- &c{-fly(X)}. fly(X) :- &c{not fly(X)}. fly(X) :- &c{fly(X)}. p(q, X) :- &c{p(q, X)}.' \
                  'a :- &c{b}. a :- &c{not c}.'
        preprocessor.preprocess(program)
