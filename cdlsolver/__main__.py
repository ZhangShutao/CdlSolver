# import clingo.ast
import sys

from cdlsolver.control.control import Control
# import heapq
import logging
import argparse
from time import perf_counter as timer


__version__ = '0.1.6'


def main():

    logging.basicConfig(encoding='utf-8', level=logging.ERROR)
    # print('CDLSolver with show statements')
    print(f'CDLSolver version: {__version__}')
    argparser = argparse.ArgumentParser(prog='cdlsolver')
    argparser.add_argument('input_files', nargs='+', type=str, help='path to input files')
    args = argparser.parse_args()

    start = timer()
    control = Control()

    try:
        for file_path in args.input_files:
            control.load(file_path)
    except SyntaxError as e:
        sys.stderr.write(e.msg)
        return

    model_cnt = 0
    sys.stdout.write('Solving...\n')
    try:
        for model in control.solve():
            model_cnt += 1
            sys.stdout.write(f'default model: {model_cnt}\n{model}\n')

        if model_cnt == 0:
            sys.stdout.write('Unsatisfiable\n')
        else:
            sys.stdout.write('Satisfiable\n')
    except RuntimeError as e:
        sys.stderr.write(str(e) + '\n')

    end = timer()
    sys.stdout.write(f'\nElapsed time: {(end - start):.6f}s\n')


if __name__ == '__main__':
    # clingo.ast.parse_string("p :- not &c{not q}.", lambda x: on_rule(x))
    # log to both console and file

    main()
