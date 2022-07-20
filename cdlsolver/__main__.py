# import clingo.ast
from cdlsolver.control.control import Control
# import heapq
import logging
import argparse
from time import perf_counter as timer


__version__ = '0.1.0'


def main():

    logging.basicConfig(encoding='utf-8', level=logging.WARNING)
    print(f'CDLSolver version: {__version__}')
    argparser = argparse.ArgumentParser(prog='cdlsolver')
    argparser.add_argument('input_files', nargs='+', type=str, help='path to input files')
    args = argparser.parse_args()

    start = timer()
    control = Control()

    for file_path in args.input_files:
        control.load(file_path)

    model_cnt = 0
    print('Solving...')
    for model in control.solve():
        model_cnt += 1
        print(f'default model: {model_cnt}\n{model}')

    if model_cnt == 0:
        print('Unsatisfiable')
    else:
        print('Satisfiable')

    end = timer()
    print(f'Elapsed time: {(end - start):.6f}s')


if __name__ == '__main__':
    # clingo.ast.parse_string("p :- not &c{not q}.", lambda x: on_rule(x))
    # log to both console and file

    main()





