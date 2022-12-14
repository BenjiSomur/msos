import fitness as ft
import random as rnd
import numpy as np
from copy import deepcopy
rnd.seed()


def roulette(_pop):
    _tot_fitness = 0
    _evs = []
    _parents = []
    for _indiv in _pop:
        _tot_fitness += _indiv[1]

    for _indiv in _pop:
        _evs.append(_indiv[1] / _tot_fitness)

    while len(_parents) < len(_pop):
        r = rnd.uniform(0, _tot_fitness)
        _sum = 0
        for _indx, _val in enumerate(_evs):
            _sum += _val
            if _sum >= r:
                _parents.append(_indx)
                break
    rnd.shuffle(_parents)
    return _parents


def _get_closest_0(_os):
    for _indx, _val in enumerate(_os):
        if _val == 0:
            return _indx
    return None


def crossover(_parents, _ref, _cp):
    _p1 = deepcopy(_parents[0])
    _p2 = deepcopy(_parents[1])
    if rnd.uniform(0, 1) > _cp:
        return [_p1, _p2]

    _workpieces = list(range(1, _ref['workpieces']+1))
    rnd.shuffle(_workpieces)
    _i = rnd.randint(1, len(_workpieces) - 1)
    j1 = _workpieces[:_i]
    j2 = _workpieces[_i:]
    _os1 = _p1[0][:]
    _os2 = _p2[0][:]
    _os_s1 = [0] * len(_os1)
    _os_s2 = [0] * len(_os2)
    for _indx, (_val1, _val2) in enumerate(zip(_os1, _os2)):
        if _val1 in j1:
            _os_s1[_indx] += _val1
        if _val2 in j2:
            _os_s2[_indx] += _val2
    for _val1, _val2 in zip(_os1, _os2):
        if _val1 not in j2:
            _indx = _os_s2.index(0)
            _os_s2[_indx] += _val1
        if _val2 not in j1:
            _indx = _os_s1.index(0)
            _os_s1[_indx] += _val2
    _ms1 = _p1[1][:]
    _ms2 = _p2[1][:]
    _ms_s1 = [0] * len(_ms1)
    _ms_s2 = [0] * len(_ms2)
    _ref = [rnd.randint(0, 1) for _ in range(len(_ms1))]

    for _indx, _val in enumerate(_ref):
        if _val == 0:
            _ms_s1[_indx] += _ms1[_indx]
            _ms_s2[_indx] += _ms2[_indx]
        else:
            _ms_s1[_indx] += _ms2[_indx]
            _ms_s2[_indx] += _ms1[_indx]
    _offspring = [[_os_s1, _ms_s1], [_os_s2, _ms_s2]]

    return _offspring


def _get_workpiece(_indx, _ref):
    _aux = 0
    for _key in _ref['no_process'].keys():
        _aux += _ref['no_process'][_key]
        if _indx < _aux:
            _indaux = _aux - _indx
            return [_key, _ref['no_process'][_key] - _indaux]
    return None


def _is_mutable(_machines):
    _count = _machines.count(0)
    if _count < len(_machines) - 2:
        return True
    return False


def _get_times(_job, _indx, _ref):
    _min = max(_ref['process_time'][_job][_indx])
    _indaux = 0
    for _indx, _val in enumerate(_ref['process_time'][_job][_indx]):
        if _val < _min:
            _indaux = _indx
    return _indaux + 1


def get_possible_machines(_ref, _job, _indx):
    machs = []
    for idx, val in enumerate(_ref['process_time'][_job][_indx]):
        if val > 0:
            machs.append(idx)
    return machs


def mutation(_chrom, _ref, _mp):
    _os = _chrom[0][:]
    _ms = _chrom[1][:]
    if rnd.uniform(0, 1) > _mp:
        return [_os, _ms]

    _pos1 = rnd.randint(0, len(_os) - 1)
    _pos2 = rnd.randint(0, len(_os) - 1)
    a = _os[_pos1]
    b = _os[_pos2]
    _os[_pos1] = b
    _os[_pos2] = a

    _pos = rnd.randint(0, len(_ms)-1)
    _job, _indx = _get_workpiece(_pos, _ref)
    _machs = get_possible_machines(_ref, _job, _indx)
    while True:
        _selected = rnd.sample(_machs, 1)[0]
        if _selected != _ms[_pos]:
            _ms[_pos] = _selected + 1
            break

    return [_os, _ms]


def repair_sol(_chrom, _ref):
    _os = _chrom[0]
    _ms = _chrom[1]
    for _indx, _machine in enumerate(_ms):
        _job, _indaux = _get_workpiece(_indx, _ref)
        if _ref['process_time'][_job][_indaux][_machine - 1] > 0:
            continue
        while True:
            _pos = rnd.randint(0, _ref['no_machines'] - 1)
            if _ref['process_time'][_job][_indaux][_pos] > 0:
                _ms[_indx] = _pos + 1
                break
    return [_os, _ms]
