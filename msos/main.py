from matplotlib import pyplot as plt
from operator import itemgetter
import operators as op
import fitness as ft
import random as rnd
import argparse
import json
import sys
import os


def _initialize_pop(_ref, _pop_size):
    _pop = []
    while len(_pop) < _pop_size:
        _indiv = []
        _os = []
        _ms = []
        for _indx, _key in enumerate(_ref['no_process'].keys()):
            for _ in range(_ref['no_process'][_key]):
                _os.append(_indx+1)
        rnd.shuffle(_os)
        while len(_ms) < len(_os):
            _job, _indx = op._get_workpiece(len(_ms), _ref)
            machs = op.get_possible_machines(_ref, _job, _indx)
            if len(machs) >= 2:
                m1, m2 = rnd.sample(machs, 2)
                _aux_ref = _ref['process_time'][_job][_indx]
                if _aux_ref[m1] > _aux_ref[m2] and rnd.uniform(0, 1) < 0.8:
                    _ms.append(m1 + 1)
                else:
                    _ms.append(m2 + 1)
            else:
                _ms.append(machs[0] + 1)
        _pop.append([_os, _ms])
    return _pop


def _evaluate(_pop, _ref):
    _new_pop = []
    for _indiv in _pop:
        _tasks = ft.decoding(_indiv, _ref)
        _schdl = ft.create_schedule(_tasks, _ref)
        _fitness = ft.get_fitness(_schdl)
        _new_pop.append([_indiv, _fitness])
    return _new_pop


def main(filename, pop_size, cp, mp, no_gen):
    with open('./Instances/{}.json'.format(filename), 'r') as f:
        _aux = json.load(f)
    ref = _aux['machine']

    gen = 0
    _pop = _initialize_pop(ref, pop_size)
    _pop = _evaluate(_pop, ref)
    _pop = sorted(_pop, key=itemgetter(1))

    while gen < no_gen:
        parents = op.roulette(_pop)
        offsp = list()
        for i in range(0, len(parents), 2):
            p1 = _pop[parents[i]][0]
            p2 = _pop[parents[i+1]][0]
            offspring = op.crossover([p1, p2], ref, cp)
            chld1 = op.mutation(offspring[0], ref, mp)
            chld2 = op.mutation(offspring[1], ref, mp)
            offsp += [chld1, chld2]

        for indiv in offsp:
            tasks = ft.decoding(indiv, ref)
            schdl = ft.create_schedule(tasks, ref)
            fitness = ft.get_fitness(schdl)
            _pop.append([indiv, fitness])
        del offsp
        _pop = sorted(_pop, key=itemgetter(1))
        while len(_pop) > pop_size:
            _pop.pop(0)
        gen += 1

    _best = _pop[-1][0]
    _best_fitness = _pop[-1][1]
    return _best_fitness


if __name__ == '__main__':
    ap = argparse.ArgumentParser(
        description='FJSP algorithm with paired list encoding')
    ap.add_argument("--pop_size", dest='pop_size',
                    type=int, help="Population size")
    ap.add_argument("--cp", dest='cp', type=float,
                    help="Crossover probability")
    ap.add_argument('--mp', dest='mp', type=float, help='Mutation probability')
    ap.add_argument('--no_gen', dest='no_gen', type=int,
                    help='Max no. of generations')
    ap.add_argument('--i', dest='filename', type=str,
                    help='Instance of benchmark to be evaluated')
    ap.add_argument('--s', dest='seed', type=float, help='Seed value')
    args = ap.parse_args()

    rnd.seed(args.seed)

    print(main(args.filename, args.pop_size, args.cp, args.mp, args.no_gen))
