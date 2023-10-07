import unittest
import clingo
import clingo.ast
import clingox.program
from clingox.program import ProgramObserver


class VisitTransformer(clingo.ast.Transformer):

    def visit_Literal(self, literal):
        print("visiting literal " + str(literal))
        print(literal.atom.ast_type)
        # print(literal.atom.keys)
        for argument in literal.atom.symbol.arguments:
            print(argument.operator_type)
        return literal

    # def visit_Rule(self, rule):
    #     print("visiting rule " + str(rule))
    #     print(rule.head.ast_type)
    #     if rule.head.ast_type == clingo.ast.ASTType.Disjunction:
    #         print(rule.head.elements[0].literal.atom.symbol.ast_type)
    #     # print(rule.head.keys)
    #     return rule

    # def visit_Program(self, program):
        # print(program.keys)


@unittest.skip('skip is upper.')
class TestClingo(unittest.TestCase):

    def test_ground(self):
        ctl = clingo.Control()
        with clingo.ast.ProgramBuilder(ctl) as bld:
            clingo.ast.parse_string('fly(X):-bird(X),not -fly(X). bird(tweety). #show fly/1.', bld.add)
        ctl.ground([('base', [])])
        for atom in ctl.symbolic_atoms:
            print(atom.symbol)

    def test_program_construct(self):
        ctl = clingo.Control(arguments=[f"--models=0"])
        with clingo.ast.ProgramBuilder(ctl) as bld:

            pos = clingo.ast.Position('<string>', 1, 1)
            loc = clingo.ast.Location(pos, pos)

            x = clingo.ast.Variable(loc, 'X')
            guess = clingo.ast.SymbolicAtom(clingo.ast.Function(loc, 'guess_fly', [x], False))
            p_guess = clingo.ast.ConditionalLiteral(loc, clingo.ast.Literal(loc, clingo.ast.Sign.NoSign, guess), [])
            n_guess = clingo.ast.ConditionalLiteral(loc, clingo.ast.Literal(loc, clingo.ast.Sign.Negation, guess), [])
            guesses = clingo.ast.Disjunction(loc, [p_guess, n_guess])

            bird = clingo.ast.SymbolicAtom(clingo.ast.Function(loc, 'bird', [x], False))
            nfly = clingo.ast.SymbolicAtom(clingo.ast.Function(loc, '-fly', [x], False))
            # body_lit = clingo.ast.Literal(loc, clingo.ast.Sign.NoSign, clingo.ast.SymbolicAtom(bird))
            body = [clingo.ast.Literal(loc, clingo.ast.Sign.NoSign, bird), clingo.ast.Literal(loc, clingo.ast.Sign.Negation, nfly)]
            rule = clingo.ast.Rule(loc, guesses,  body)
            print(rule)
            bld.add(rule)

            # trm = VisitTransformer()
            t = clingo.ast.Function(loc, 'tweety', [], False)
            tbird = clingo.ast.SymbolicAtom(clingo.ast.Function(loc, 'bird', [t], False))
            fact = clingo.ast.Rule(loc, clingo.ast.Literal(loc, clingo.ast.Sign.NoSign, tbird), [])
            # print(fact)
            bld.add(fact)

            fly = clingo.ast.SymbolicAtom(clingo.ast.Function(loc, '-fly', [x], False))
            false_term = clingo.ast.SymbolicTerm(loc, clingo.symbol.Function('false', [], True))
            external = clingo.ast.External(loc, fly, body, false_term)
            print(external)
            bld.add(external)

        ctl.ground([('base', [])])
        ctl.assign_external(clingo.symbol.Function('-fly', [clingo.symbol.Function('tweety', [])]), True)
        for model in ctl.solve(yield_=True):
            print(model)

    def test_clingo(self):
        vtm = VisitTransformer()
        ctl = clingo.Control(arguments=[f"--models=0"])
        with clingo.ast.ProgramBuilder(ctl) as bld:
            clingo.ast.parse_string('time(T+1):- time(T).', vtm)
            clingo.ast.parse_string('guess(X) | not guess(X) :- bird(X). bird(tweety).', bld.add)
        ctl.ground([('base', [])])

        with ctl.solve(yield_=True) as handle:
            for model in handle:
                symbols = model.symbols(shown=True)
                print(model)
                print(symbols[0].arguments[0].type)

    def test_constraint(self):
        ctl = clingo.Control(['0'])

        pos = clingo.ast.Position('<string>', 1, 1)
        loc = clingo.ast.Location(pos, pos)

        false = clingo.ast.BooleanConstant(0)
        head = clingo.ast.Literal(loc, clingo.ast.Sign.NoSign, false)

        x = clingo.ast.Variable(loc, 'X')
        bird = clingo.ast.SymbolicAtom(clingo.ast.Function(loc, 'bird', [x], False))
        body = [clingo.ast.Literal(loc, clingo.ast.Sign.NoSign, bird)]

        fly = clingo.ast.SymbolicAtom(clingo.ast.Function(loc, 'fly', [x], False))

        constraint = clingo.ast.Rule(loc, head, body)
        rule = clingo.ast.Rule(loc, clingo.ast.Literal(loc, clingo.ast.Sign.NoSign, fly), body)

        print(constraint)
        with clingo.ast.ProgramBuilder(ctl) as bld:
            bld.add(constraint)

        ctl.add('base', [], 'bird(tweety).')
        ctl.ground([('base', [])])
        print(ctl.solve(on_model=print))

    def test_assumption(self):
        ctl = clingo.Control(['0'])
        with open('E:/Projects/cdlsolver/test/test_programs/temp.lp', 'r') as program_file:
            ctl.add('base', [], program_file.read())
        ctl.ground([('base', [])])

        assumptions = []
        assumptions.append((clingo.symbol.Function('apply', [clingo.symbol.Function('r1'), clingo.symbol.Number(1)]), True))
        assumptions.append((clingo.symbol.Function('napply', [clingo.symbol.Function('p1')]), True))
        # assumptions.append((clingo.symbol.Function('p', [clingo.symbol.Number(1)]), True))
        # assumptions.append((clingo.symbol.Function('p', [clingo.symbol.Number(2)]), True))
        # assumptions.append((clingo.symbol.Function('a', [clingo.symbol.Number(1)]), True))
        # assumptions.append((clingo.symbol.Function('guess_not_apply', [clingo.symbol.Function('r1'), clingo.symbol.Number(2)]), True))
        # assumptions.append((clingo.symbol.Function('guess_napply', [clingo.symbol.Function('p1')]), True))
        # assumptions.append((clingo.symbol.Function('ok'), True))

        with ctl.solve(yield_=True, assumptions=assumptions) as handle:
            print(handle.get())
            cnt = 0
            for m in handle:
                print(m)
                cnt += 1
            print(cnt)

    def test_external(self):
        ctl = clingo.Control(['0'])
        ctl.add('base', [], ':- a(X). p(1).')
        ctl.add('base', [], '#external a(X) : p(X).')
        ctl.ground([('base', [])])

        ctl.assign_external(clingo.symbol.Function('a', [clingo.symbol.Number(1)]), False)
        print(ctl.solve(on_model=print))

        ctl.assign_external(clingo.symbol.Function('a', [clingo.symbol.Number(1)]), True)
        print(ctl.solve(on_model=print))

        ctl.release_external(clingo.symbol.Function('a', [clingo.symbol.Number(1)]))
        print(ctl.solve(on_model=print))

    def test_theory_atom(self):
        ctl = clingo.Control(['0'])
        ctl.add('base', [], 'a :- not &c{-b}.')
        ctl.ground(([('base', [])]))

        print(ctl.solve(on_model=print))

    def _parse_log_callback(self, message_code, msg):
        self._error = True
        self._error_msg = msg

    def test_parse_grammar_error(self):
        error = False
        error_msg = ""

        program = "a :- b"
        try:
            clingo.ast.parse_string(program, print, logger=lambda msg_code, msg: self._parse_log_callback(msg_code, msg))
        except RuntimeError as e:
            print(str(self._error_msg))
        print("after parsing")

    def test_output_ground(self):
        prog = clingox.program.Program()
        program = "p :- q. r :- guess_q. :- p."
        choice = "guess_q | not guess_q."
        ctl = clingo.Control(['--enum-mode=cautious', '0'])
        ctl.register_observer(ProgramObserver(prog))
        ctl.add('base', [], program)
        # ctl.ground(([('base', [])]))
        ctl.add('choice', [], choice)
        ctl.ground(([('base', []), ('choice', [])]))
        print(prog)
        ctl.solve(on_model=print)
