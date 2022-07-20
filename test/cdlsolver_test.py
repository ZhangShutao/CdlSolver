import io

from cdlsolver.control.control import Control
import unittest

BASIC_TEST = ['E:/Projects/cdlsolver/test/test_programs/basic_test.lp']
BASIC_TEST_OUT = 'E:/Projects/cdlsolver/test/test_programs/basic_test.out'

BIRD_TEST = ['E:/Projects/cdlsolver/test/test_programs/bird.lp']
BIRD_TEST_OUT = 'E:/Projects/cdlsolver/test/test_programs/bird.out'

RACE_TEST = ['E:/Projects/cdlsolver/test/test_programs/race.lp']
RACE_TEST_OUT = 'E:/Projects/cdlsolver/test/test_programs/race.out'

DN_1_TEST = ['E:/Projects/cdlsolver/test/test_programs/negation_and_default_1.lp']
DN_1_TEST_OUT = 'E:/Projects/cdlsolver/test/test_programs/negation_and_default_1.out'

DN_2_TEST = ['E:/Projects/cdlsolver/test/test_programs/negation_and_default_2.lp']
DN_2_TEST_OUT = 'E:/Projects/cdlsolver/test/test_programs/negation_and_default_2.out'


class ControlTest(unittest.TestCase):

    def _get_x_y(self, str):
        parts = str.strip().replace(' ', '').split(';')
        x = set(parts[0].replace('x:', '').split(','))
        y = set(parts[1].replace('y:', '').split(','))
        return x, y

    def _test_control(self, paths, out):
        control = Control()

        for file_path in paths:
            control.load(file_path)

        output = io.StringIO()
        model_cnt = 0
        models = control.solve()
        for model in models:
            # print(model.__class__.__name__)
            model_cnt += 1
            print(f'default model: {model_cnt}\n{model}', file=output)

        if model_cnt == 0:
            print('Unsatisfiable', file=output)
        else:
            print('Satisfiable', file=output)

        print(output.getvalue())

        with open(out, 'r') as out_file:
            lines = output.getvalue().splitlines()
            std_out = out_file.readlines()

            for i in range(len(lines)):
                self.assertIsNotNone(std_out[i])
                if lines[i].startswith('default model') or lines[i].startswith('Satisfiable') \
                        or lines[i].startswith('Unsatisfiable'):
                    self.assertEqual(lines[i].strip(), std_out[i].strip())
                else:
                    self.assertEqual(self._get_x_y(lines[i]), self._get_x_y(std_out[i]))

        output.close()

    def test_basic(self):
        self._test_control(BASIC_TEST, BASIC_TEST_OUT)

    def test_bird(self):
        self._test_control(BIRD_TEST, BIRD_TEST_OUT)

    def test_race(self):
        self._test_control(RACE_TEST, RACE_TEST_OUT)

    def test_negation_and_default_1(self):
        self._test_control(DN_1_TEST, DN_1_TEST_OUT)

    def test_negation_and_default_2(self):
        self._test_control(DN_2_TEST, DN_2_TEST_OUT)
