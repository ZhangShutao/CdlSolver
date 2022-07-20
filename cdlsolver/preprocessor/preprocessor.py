from abc import ABC
import clingo.ast
import logging
from clingo.ast import ProgramBuilder
from clingo.ast import Transformer


# import cdlsolver.util.util as util


class DefaultTransformer(Transformer):

    def __init__(self, defaults, additional_rules):
        self._defaults = defaults
        self._additional_rules = additional_rules

    def visit_Literal(self, literal):
        logging.debug("visiting literal: " + str(literal))

        # if str(literal) == 'bird(X)':
        #     print(literal.atom.symbol.operator_type == clingo.ast.UnaryOperator.Minus)

        if self._is_default_literal(literal):
            guess_literal = self._get_guess_literal(literal)
            self._defaults.add(self._get_positive_literal(guess_literal))

            for fc in self._get_fact_constraint(literal):  # fact constraint
                self._additional_rules.append(fc)

            for wnc in self._get_weak_negation_constraint(literal):
                self._additional_rules.append(wnc)

            for snc in self._get_strong_negation_constraint(literal):
                self._additional_rules.append(snc)

            logging.debug("output literal:" + str(guess_literal))
            return guess_literal
        else:
            logging.debug("output literal:" + str(literal))
            return literal

    def visit_Rule(self, rule):
        logging.debug("visiting rule: " + str(rule))
        if rule.ast_type == clingo.ast.ASTType.Rule and rule.body:
            # pos_body = self._get_positive_body(rule)
            for literal in rule.body:
                if self._is_default_literal(literal):
                    choose_rule = self._get_choice_rule(rule, literal)
                    self._additional_rules.append(choose_rule)
        ret = rule.update(**self.visit_children(rule))
        logging.debug("output rule:" + str(ret))
        return ret

    def _contains_default_literal(self, body):
        for literal in body:
            if self._is_default_literal(literal):
                return True
        return False

    def _is_default_literal(self, ast):
        """
        return true if this ast node is a default literal

        :param ast:
        :return:
        """
        return ast.ast_type == clingo.ast.ASTType.Literal \
               and ast.atom.ast_type == clingo.ast.ASTType.TheoryAtom \
               and 'c' == ast.atom.term.name

    def _get_positive_body(self, rule):
        pos_body = []
        for literal in rule.body:
            if literal.ast_type == clingo.ast.ASTType.Literal and not self._is_default_literal(literal):
                if literal.sign != clingo.ast.Sign.Negation and literal.sign != clingo.ast.Sign.DoubleNegation:
                    pos_body.append(literal)
        return pos_body

    def _get_choice_rule(self, rule, literal):
        """
        A choice rule is an ASP rule with a pair of opposite guess literals. For example, a choice rule of
        {fly(X):- bird(X), &c{fly(x)}} w.r.t &c{fly(X)} is
        guess_fly(X) | not guess_fly(X) :- bird(X).

        :param rule:
        :param literal:
        :return:
        """
        guess_name, guess_args = self._get_default_name_and_args(literal)
        guess_atom = clingo.ast.SymbolicAtom(clingo.ast.Function(literal.location, guess_name, guess_args, False))
        pos_guess = clingo.ast.ConditionalLiteral(literal.location,
                                                  clingo.ast.Literal(literal.location, clingo.ast.Sign.NoSign,
                                                                     guess_atom), [])
        neg_guess = clingo.ast.ConditionalLiteral(literal.location,
                                                  clingo.ast.Literal(literal.location, clingo.ast.Sign.Negation,
                                                                     guess_atom), [])
        heads = clingo.ast.Disjunction(literal.location, [pos_guess, neg_guess])
        return clingo.ast.Rule(rule.location, heads, self._get_positive_body(rule))

    # def _get_weak_negation_constraint(self, literal):
    #     return clingo.ast.Rule(literal.location, )

    def _get_fact_constraint(self, literal):
        """
        for a default literal &c{l} or &c{-l}, there is a constraint rule that {:- guess_not_l, l.}
        or {:- guess_not_sn_l, -l}
        :param literal:
        :return: a set of addition rules with fact constraint of 'literal'
        """
        if self._is_default_literal(literal):
            # is_negation = False
            theory_term = literal.atom.elements[0].terms[0]
            if theory_term.ast_type == clingo.ast.ASTType.TheoryUnparsedTerm:
                if 'not' in theory_term.elements[0].operators or '~' in theory_term.elements[0].operators:
                    return []

            guess_name, guess_args = self._get_default_name_and_args(literal)
            guess_atom = clingo.ast.SymbolicAtom(
                clingo.ast.Function(literal.location, guess_name.replace('guess_', 'guess_not_'), guess_args, False))
            neg_guess = clingo.ast.Literal(literal.location, clingo.ast.Sign.NoSign, guess_atom)

            pos_literal = self._get_objective_literal_from_default(literal)
            # print(neg_guess_name)

            return [self._get_constraint([neg_guess, pos_literal])]
        return []

    def _get_weak_negation_constraint(self, literal):
        if self._is_default_literal(literal):
            guess_name, guess_args = self._get_default_name_and_args(literal)
            pos_guess_name = guess_name.replace('guess_not_', 'guess_')
            neg_guess_name = pos_guess_name.replace('guess_', 'guess_not_')

            pos_guess = clingo.ast.Literal(literal.location, clingo.ast.Sign.NoSign,
                                           clingo.ast.SymbolicAtom(clingo.ast.Function(literal.location, pos_guess_name,
                                                                                       guess_args, False)))
            neg_guess = clingo.ast.Literal(literal.location, clingo.ast.Sign.NoSign,
                                           clingo.ast.SymbolicAtom(clingo.ast.Function(literal.location, neg_guess_name,
                                                                                       guess_args, False)))
            return [self._get_constraint([pos_guess, neg_guess])]
        else:
            return []

    def _get_strong_negation_constraint(self, literal):
        if self._is_default_literal(literal):
            guess_name, guess_args = self._get_default_name_and_args(literal)
            pos_guess_name = guess_name.replace('guess_not_', 'guess_').replace('guess_sn_', 'guess_')
            neg_guess_name = pos_guess_name.replace('guess_', 'guess_sn_')

            pos_guess = clingo.ast.Literal(literal.location, clingo.ast.Sign.NoSign,
                                           clingo.ast.SymbolicAtom(clingo.ast.Function(literal.location, pos_guess_name,
                                                                                       guess_args, False)))
            neg_guess = clingo.ast.Literal(literal.location, clingo.ast.Sign.NoSign,
                                           clingo.ast.SymbolicAtom(clingo.ast.Function(literal.location, neg_guess_name,
                                                                                       guess_args, False)))
            return [self._get_constraint([pos_guess, neg_guess])]

        else:
            return []

    def _get_constraint(self, body):
        pos = clingo.ast.Position('<string>', 1, 1)
        loc = clingo.ast.Location(pos, pos)

        false = clingo.ast.BooleanConstant(0)
        head = clingo.ast.Literal(loc, clingo.ast.Sign.NoSign, false)

        return clingo.ast.Rule(loc, head, body)

    def _get_guess_literal(self, literal):
        """
        get the guess form of a default literal

        :param literal: the default literal
        :return: the guess form of the input, for example, &c{a} -> guess_a, &c{not -a} -> guess_not_sn_a
        """
        logging.debug('default: ' + str(literal))
        guess_sig = literal.sign
        guess_name, guess_args = self._get_default_name_and_args(literal)

        symbolic_atom = clingo.ast.SymbolicAtom(clingo.ast.Function(literal.location, guess_name, guess_args, False))
        return clingo.ast.Literal(literal.location, guess_sig, symbolic_atom)

    def _get_objective_literal_from_default(self, literal):
        theory_term = literal.atom.elements[0].terms[0]
        if theory_term.ast_type == clingo.ast.ASTType.SymbolicTerm:
            atom = clingo.ast.SymbolicAtom(clingo.ast.Function(literal.location, theory_term.symbol.name, [], False))
        elif theory_term.ast_type == clingo.ast.ASTType.TheoryFunction:
            # print(theory_term.ast_type)
            atom = clingo.ast.SymbolicAtom(clingo.ast.Function(literal.location, theory_term.name,
                                                               [self._get_theory_function_argument(symbol_argument)
                                                                for symbol_argument in theory_term.arguments], False))
        elif theory_term.ast_type == clingo.ast.ASTType.TheoryUnparsedTerm:
            theory_element = theory_term.elements[0]
            element_term = theory_element.term
            if element_term.ast_type == clingo.ast.ASTType.SymbolicTerm:
                function = clingo.ast.Function(literal.location, element_term.symbol.name, [], False)
            elif element_term.ast_type == clingo.ast.ASTType.TheoryFunction:
                # print(element_term.ast_type)
                function = clingo.ast.Function(literal.location, element_term.name,
                                               [self._get_theory_function_argument(symbol_argument)
                                                for symbol_argument in element_term.arguments], False)
            else:
                raise RuntimeError('wrong type of default literal: ' + str(literal))

            if '-' in theory_element.operators:
                atom = clingo.ast.SymbolicAtom(
                    clingo.ast.UnaryOperation(literal.location, clingo.ast.UnaryOperator.Minus, function))
            else:
                atom = clingo.ast.SymbolicAtom(function)
        else:
            raise RuntimeError('wrong type of default literal: ' + str(literal))

        return clingo.ast.Literal(literal.location, clingo.ast.Sign.NoSign, atom)

    def _get_default_name_and_args(self, literal):
        """
        Get the name and arguments of a default literal
        :param literal:
        :return: name(str), arguments(list)
        """
        theory_term = literal.atom.elements[0].terms[0]

        if theory_term.ast_type == clingo.ast.ASTType.SymbolicTerm:
            return 'guess_' + str(theory_term.symbol.name), []
        elif theory_term.ast_type == clingo.ast.ASTType.TheoryFunction:
            return 'guess_' + str(theory_term.name), [self._get_theory_function_argument(symbol_argument)
                                                      for symbol_argument in theory_term.arguments]
        elif theory_term.ast_type == clingo.ast.ASTType.TheoryUnparsedTerm:
            theory_element = theory_term.elements[0]

            literal_name = 'guess_'
            for operator in theory_element.operators:
                if operator == '~' or operator == 'not':
                    literal_name += 'not_'
                elif operator == '-':
                    literal_name += 'sn_'

            element_term = theory_element.term
            logging.debug('theory element term: ' + str(element_term.ast_type))
            if element_term.ast_type == clingo.ast.ASTType.SymbolicTerm:
                return literal_name + str(element_term.symbol.name), []
            elif element_term.ast_type == clingo.ast.ASTType.TheoryFunction:
                return literal_name + str(element_term.name), [self._get_theory_function_argument(symbol_argument)
                                                               for symbol_argument in element_term.arguments]

        raise RuntimeError('unknown type of default literal ' + str(literal))

    def _get_theory_function_argument(self, argument):
        # print(argument.ast_type)
        if argument.ast_type == clingo.ast.ASTType.TheoryFunction:
            return clingo.ast.Function(argument.location, argument.name,
                                       [self._get_theory_function_argument(arg)
                                        for arg in argument.arguments], False)
        else:
            return argument

    def _get_positive_literal(self, literal):
        return clingo.ast.Literal(literal.location, clingo.ast.Sign.NoSign, literal.atom)


class Preprocessor(ABC):

    def __init__(self, defaults, candidate_ctl, test_ctl):
        self._defaults = defaults
        self._candidate_ctl = candidate_ctl
        self._test_ctl = test_ctl
        self._additional_rules = []
        # self._guesses = guesses

    def preprocess(self, program):
        default_transformer = DefaultTransformer(self._defaults, self._additional_rules)
        # guess_ctl = clingo.Control()
        clingo.ast.parse_string(program, lambda ast: self._add_to_controls(default_transformer(ast)))
        for rule in self._additional_rules:
            self._add_to_controls(rule)
        # with clingo.ast.ProgramBuilder(self._candidate_ctl) as builder:
        #     clingo.ast.parse_string(program, lambda ast: builder.add(default_transformer(ast)))
        #     for rule in self._additional_rules:
        #         builder.add(rule)
            # clingo.ast.parse_string(program, default_transformer)

        # guess_ctl.ground([('ground', [])])
        # print(guess_ctl)
        return 0

    def _add_to_controls(self, ast):
        for control in [self._candidate_ctl, self._test_ctl]:
            with ProgramBuilder(control) as builder:
                builder.add(ast)
