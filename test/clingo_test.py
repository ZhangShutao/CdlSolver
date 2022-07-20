import unittest
import clingo
import clingo.ast


class VisitTransformer(clingo.ast.Transformer):

    def visit_Literal(self, literal):
        print("visiting literal " + str(literal))
        # print(literal.atom)
        # print(literal.atom.keys)
        return literal

    def visit_Rule(self, rule):
        print("visiting rule " + str(rule))
        print(rule.head.ast_type)
        if rule.head.ast_type == clingo.ast.ASTType.Disjunction:
            print(rule.head.elements[0].literal.atom.symbol.ast_type)
        print(rule.head.keys)
        return rule

    def visit_Program(self, program):
        print(program.keys)


class TestClingo(unittest.TestCase):

    def test_ground(self):
        ctl = clingo.Control()
        with clingo.ast.ProgramBuilder(ctl) as bld:
            clingo.ast.parse_string('fly(X):-bird(X),not -fly(X). bird(tweety).', bld.add)
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
            # body_lit = clingo.ast.Literal(loc, clingo.ast.Sign.NoSign, clingo.ast.SymbolicAtom(bird))
            body = [clingo.ast.Literal(loc, clingo.ast.Sign.NoSign, bird)]
            rule = clingo.ast.Rule(loc, guesses,  body)
            print(rule)
            bld.add(rule)

            # trm = VisitTransformer()
            t = clingo.ast.Function(loc, 'tweety', [], False)
            tbird = clingo.ast.SymbolicAtom(clingo.ast.Function(loc, 'bird', [t], False))
            fact = clingo.ast.Rule(loc, clingo.ast.Literal(loc, clingo.ast.Sign.NoSign, tbird), [])
            # print(fact)
            bld.add(fact)

        ctl.ground([('base', [])])
        for model in ctl.solve(yield_=True):
            print(model)

    def test_clingo(self):
        vtm = VisitTransformer()
        ctl = clingo.Control(arguments=[f"--models=0"])
        with clingo.ast.ProgramBuilder(ctl) as bld:
            clingo.ast.parse_string('guess(X) | not guess(X) :- bird(X). bird(tweety).', vtm)
            clingo.ast.parse_string('guess(X) | not guess(X) :- bird(X). bird(tweety).', bld.add)
        ctl.ground([('base', [])])

        with ctl.solve(yield_=True) as handle:
            for model in handle:
                symbols = model.symbols(shown=True)
                print(model)
                print(symbols[0].arguments[0].type)

    def test_constraint(self):
        ctl = clingo.Control(['0'])
        vtm = VisitTransformer()
        with clingo.ast.ProgramBuilder(ctl) as bld:
            clingo.ast.parse_string(':-a(X), b(X).', vtm)

        ctl.cleanup()

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

