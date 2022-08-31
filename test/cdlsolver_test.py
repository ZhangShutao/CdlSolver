import io

from cdlsolver.control.control import Control
import unittest
import logging
from time import perf_counter as timer


logger = logging.getLogger()
logger.level = logging.DEBUG

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

ND_TEST = ['E:/Projects/cdlsolver/test/test_programs/negative_default.lp']
ND_TEST_OUT = 'E:/Projects/cdlsolver/test/test_programs/negative_default.out'

MULTI_INPUT_TEST = ['E:/Projects/cdlsolver/test/test_programs/multi_in_1.lp',
                    'E:/Projects/cdlsolver/test/test_programs/multi_in_2.lp']
MULTI_INPUT_OUT = 'E:/Projects/cdlsolver/test/test_programs/multi_in.out'

CR_1_TEST = ['E:/Projects/cdlsolver/test/test_programs/cr_1.lp']
CR_1_TEST_OUT = 'E:/Projects/cdlsolver/test/test_programs/cr_1.out'

CR_2_TEST = ['E:/Projects/cdlsolver/test/test_programs/cr_2.lp']
CR_2_TEST_OUT = 'E:/Projects/cdlsolver/test/test_programs/cr_2.out'

CR_3_TEST = ['E:/Projects/cdlsolver/test/test_programs/cr_3.lp']
CR_3_TEST_OUT = 'E:/Projects/cdlsolver/test/test_programs/cr_3.out'

CR_4_TEST = ['E:/Projects/cdlsolver/test/test_programs/cr_4.lp']
CR_4_TEST_OUT = 'E:/Projects/cdlsolver/test/test_programs/cr_4.out'

CR_5_TEST = ['E:/Projects/cdlsolver/test/test_programs/cr_5.lp']
CR_5_TEST_OUT = 'E:/Projects/cdlsolver/test/test_programs/cr_5.out'

PLANNING_TEST = ['E:/Projects/cdlsolver/test/test_programs/planning.lp']
PLANNING_OUT = 'E:/Projects/cdlsolver/test/test_programs/planning.out'

PREF_TEST = ['E:/Projects/cdlsolver/test/test_programs/prefer.lp']
PREF_OUT = 'E:/Projects/cdlsolver/test/test_programs/prefer.out'

DI_TEST = ['E:/Projects/cdlsolver/test/test_programs/di-semantics.lp']
DI_TEST_OUT = 'E:/Projects/cdlsolver/test/test_programs/di-semantics.out'

LIKE_TEST = ['E:/Projects/cdlsolver/test/test_programs/icecream.lp']
LIKE_TEST_OUT = 'E:/Projects/cdlsolver/test/test_programs/icecream.out'

ABN_TEST = ['E:/Projects/cdlsolver/test/test_programs/abnormal.lp']
ABN_TEST_OUT = 'E:/Projects/cdlsolver/test/test_programs/abnormal.out'

NAF_TEST = ['E:/Projects/cdlsolver/test/test_programs/naf.lp']
NAF_TEST_OUT = 'E:/Projects/cdlsolver/test/test_programs/naf.out'


class ControlTest(unittest.TestCase):

    def _get_x_y(self, str):
        parts = str.strip().replace(' ', '').split(';')
        x = set(parts[0].replace('x:', '').split(','))
        y = set(parts[1].replace('y:', '').split(','))
        return x, y

    def _test_control(self, paths, out):
        start = timer()
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

        end = timer()
        print(f'Elapsed time: {(end - start):.6f}s')
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

    def test_negative_default(self):
        self._test_control(ND_TEST, ND_TEST_OUT)

    def test_multi_input(self):
        self._test_control(MULTI_INPUT_TEST, MULTI_INPUT_OUT)

    def test_planning(self):
        self._test_control(PLANNING_TEST, PLANNING_OUT)

    def test_cr_1(self):
        self._test_control(CR_1_TEST, CR_1_TEST_OUT)

    def test_cr_2(self):
        self._test_control(CR_2_TEST, CR_2_TEST_OUT)

    def test_cr_3(self):
        self._test_control(CR_3_TEST, CR_3_TEST_OUT)

    def test_cr_4(self):
        self._test_control(CR_4_TEST, CR_4_TEST_OUT)

    def test_cr_5(self):
        self._test_control(CR_5_TEST, CR_5_TEST_OUT)

    def test_di(self):
        self._test_control(DI_TEST, DI_TEST_OUT)

    def test_prefer(self):
        self._test_control(PREF_TEST, PREF_OUT)

    def test_icecream(self):
        self._test_control(LIKE_TEST, LIKE_TEST_OUT)

    def test_abnormal(self):
        self._test_control(ABN_TEST, ABN_TEST_OUT)

    def test_naf(self):
        self._test_control(NAF_TEST, NAF_TEST_OUT)
