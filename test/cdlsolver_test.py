import io

from cdlsolver.control.control import Control
import unittest
import logging
from time import perf_counter as timer


logger = logging.getLogger()
logger.level = logging.DEBUG

BASIC_TEST = ['E:/Projects/cdlsolver/test/test_programs/basic_test.lp']
BASIC_TEST_OUT = 'E:/Projects/cdlsolver/test/test_programs/basic_test.out'

CONS_TEST = ['E:/Projects/cdlsolver/test/test_programs/constraint.lp']
CONS_TEST_OUT = 'E:/Projects/cdlsolver/test/test_programs/constraint.out'

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

NAF_2_TEST = ['E:/Projects/cdlsolver/test/test_programs/naf_2.lp']
NAF_2_TEST_OUT = 'E:/Projects/cdlsolver/test/test_programs/naf_2.out'

BOOK_TEST = ['E:/Projects/cdlsolver/test/test_programs/book.lp']
BOOK_TEST_OUT = 'E:/Projects/cdlsolver/test/test_programs/book.out'

RAIN_TEST = ['E:/Projects/cdlsolver/test/test_programs/rain.lp']
RAIN_TEST_OUT = 'E:/Projects/cdlsolver/test/test_programs/rain.out'

INER_TEST = ['E:/Projects/cdlsolver/test/test_programs/inertia.lp']
INER_TEST_OUT = 'E:/Projects/cdlsolver/test/test_programs/inertia.out'

IN_AB_TEST = ['E:/Projects/cdlsolver/test/test_programs/indirect_abnormal.lp']
IN_AB_TEST_OUT = 'E:/Projects/cdlsolver/test/test_programs/indirect_abnormal.out'

DIR_AB_TEST = ['E:/Projects/cdlsolver/test/test_programs/direct_abnormal.lp']
DIR_AB_TEST_OUT = 'E:/Projects/cdlsolver/test/test_programs/direct_abnormal.out'

DIR_SCHOOL_TEST = ['E:/Projects/cdlsolver/test/test_programs/school.lp']
DIR_SCHOOL_TEST_OUT = 'E:/Projects/cdlsolver/test/test_programs/school.out'


class OutputModel:
    def __init__(self, x=None, y=None):
        if x is None:
            x = set()
        if y is None:
            y = set()
        self._x = x
        self._y = y

    def load(self, str):
        parts = str.strip().replace(' ', '').split(';')
        self._x = set(parts[0].replace('x:', '').split(','))
        self._y = set(parts[1].replace('y:', '').split(','))

    def __key(self):
        return ';'.join([','.join([str(x) for x in self._x]), ','.join([str(y) for y in self._y])])

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, OutputModel):
            return self._x == other._x and self._y == other._y
        return NotImplemented

    def __repr__(self):
        lis_x = [str(x) for x in self._x]
        lis_y = [str(y) for y in self._y]
        lis_x.sort()
        lis_y.sort()
        return "x:" + ','.join(lis_x) + ";y:" + ','.join(lis_y) + ";"


class Output:
    def __init__(self, models=None):
        if models is None:
            models = set()
        self._models = models

    def add(self, model):
        self._models.add(model)

    def load(self, str):
        for line in str.splitlines():
            if line.startswith('x'):
                model = OutputModel()
                model.load(line)
                self._models.add(model)

    def count(self):
        return len(self._models)

    def __eq__(self, other):
        if isinstance(other, Output):
            set_mod = set([str(m) for m in self._models])
            set_other = set([str(m) for m in other._models])
            return set_mod == set_other
        return NotImplemented


class ControlTest(unittest.TestCase):

    @staticmethod
    def _get_x_y(str):
        parts = str.strip().replace(' ', '').split(';')
        x = set(parts[0].replace('x:', '').split(','))
        y = set(parts[1].replace('y:', '').split(','))
        return x, y

    def _test_control(self, paths, out):
        start = timer()
        control = Control()

        for file_path in paths:
            control.load(file_path)

        models = control.solve()
        end = timer()
        print(f'Elapsed time: {(end - start):.6f}s')

        output = Output()
        cnt = 0
        for model in models:
            cnt += 1
            output_model = OutputModel()
            output_model.load(str(model))
            output.add(output_model)
            print(f'default model: {cnt}\n{model}')

        if output.count() == 0:
            print('Unsatisfiable')
        else:
            print('Satisfiable')

        std_output = Output()
        with open(out, 'r') as out_file:
            std_output.load(out_file.read())
            self.assertEqual(std_output, output)
            out_file.close()

    def test_basic(self):
        # reading
        self._test_control(BASIC_TEST, BASIC_TEST_OUT)

    def test_bird(self):
        self._test_control(BIRD_TEST, BIRD_TEST_OUT)

    def test_race(self):
        self._test_control(RACE_TEST, RACE_TEST_OUT)

    def test_negation_and_default_1(self):
        self._test_control(DN_1_TEST, DN_1_TEST_OUT)

    def test_negation_and_default_2(self):
        # reading
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

    # def test_cr_5(self):
    #     self._test_control(CR_5_TEST, CR_5_TEST_OUT)

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

    def test_naf_2(self):
        # reading
        self._test_control(NAF_2_TEST, NAF_2_TEST_OUT)

    def test_rain(self):
        # reading
        self._test_control(RAIN_TEST, RAIN_TEST_OUT)

    def test_book(self):
        self._test_control(BOOK_TEST, BOOK_TEST_OUT)

    def test_inertia(self):
        self._test_control(INER_TEST, INER_TEST_OUT)

    def test_constraint(self):
        # reading
        self._test_control(CONS_TEST, CONS_TEST_OUT)

    def test_indirect_abnormal(self):
        # reading
        self._test_control(IN_AB_TEST, IN_AB_TEST_OUT)

    def test_direct_abnormal(self):
        # reading
        self._test_control(DIR_AB_TEST, DIR_AB_TEST_OUT)

    def test_school(self):
        self._test_control(DIR_SCHOOL_TEST, DIR_SCHOOL_TEST_OUT)
