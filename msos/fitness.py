def _get_op(_os, _indx, _ref, _proc):
    _count = _os[_indx+1:].count(_proc)
    return _ref['no_process']['j{}'.format(_proc)] - _count


def _get_ms(_proc, _nop, _ms, _ref):
    _sum = 0
    for _key in _ref['no_process'].keys():
        if _key == 'j{}'.format(_proc):
            break
        _sum += _ref['no_process'][_key]
    return _ms[_sum + _nop - 1]


# tsk = [i,j,m,t]
# schdl[m] = [i,j,(st,et)]
def decoding(_chrom, _ref):
    _os = _chrom[0]
    _ms = _chrom[1]
    _tasks = []
    for _indx, _proc in enumerate(_os):
        _nop = _get_op(_os, _indx, _ref, _proc)
        _mindx = _get_ms(_proc, _nop, _ms, _ref)
        _t = _ref['process_time']['j{}'.format(_proc)][_nop - 1][_mindx - 1]
        _task = [_proc, _nop, 'm{}'.format(_mindx), _t]
        _tasks.append(_task)
    return _tasks


def search_prev_op(_task, _schdl):
    if _task[1] == 1:
        return None
    for _machine in _schdl.keys():
        if not _schdl[_machine]:
            continue
        for _mtask in _schdl[_machine]:
            if _mtask[1] == _task[1]-1 and _mtask[0] == _task[0]:
                return _mtask
    return False


def _get_start_time(_tsk, _schdl):
    _prev_tsk = search_prev_op(_tsk, _schdl)
    if _prev_tsk != None and _prev_tsk:
        _lst_t_time = _prev_tsk[-1][1]
    else:
        _lst_t_time = 0
    if _schdl[_tsk[2]]:
        _lst_time = _schdl[_tsk[2]][-1][-1][1]
    else:
        _lst_time = 0
    if _lst_time >= _lst_t_time:
        return _lst_time
    elif _lst_time < _lst_t_time:
        return _lst_t_time


def create_schedule(_tasks, _ref):
    _schdl = {}
    for _machine in range(_ref['no_machines']):
        _schdl['m{}'.format(_machine+1)] = list()
    for _tsk in _tasks:
        _start_time = _get_start_time(_tsk, _schdl)
        _schdl[_tsk[2]].append(
            [_tsk[0], _tsk[1], (_start_time, _start_time+_tsk[3])])
    return _schdl


def get_fitness(_schdl):
    _max = 0
    for _key in _schdl.keys():
        if not _schdl[_key]:
            continue
        if _schdl[_key][-1][-1][1] >= _max:
            _max = _schdl[_key][-1][-1][1]
    if _max > 0:
        return round(1 / _max, 5)
    else:
        return round(1/10000000, 5)

