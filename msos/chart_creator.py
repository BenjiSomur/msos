from matplotlib import pyplot as plt
from matplotlib import colors
import fitness as d
import random as rnd

rnd.seed()


def generate_colours(_ref):
    _colours = []
    for _ in range(_ref['workpieces']):
        _r = rnd.uniform(0, 1)
        _g = rnd.uniform(0, 1)
        _b = rnd.uniform(0, 1)
        _colours.append((_r, _g, _b))
    for _colour in _colours:
        yield colors.to_hex(_colour)

# gnt.broken_barh([(start_time, duration)],
#                  (lower_yaxis, height),
#                  facecolors=('tab:colours'))


def add_bar(_gnt, _task, _size, _yref, _colours):
    _start_time = _task[-1][0]
    _duration = _task[-1][1] - _start_time
    _lower_yaxis = _yref - int((_size / 2))
    _windx = _task[0] - 1
    _label = '{}/{}'.format(_task[0], _task[1])
    _gnt.broken_barh([(_start_time, _duration)],
                     (_lower_yaxis, _size),
                     facecolors=(_colours[_windx]),
                     edgecolor='black')
    _gnt.text(_start_time + 0.3, _yref, _label, c='black')


def create_graph(_indiv, _ref):
    _colours = [x for x in generate_colours(_ref)]
    _chrom = _indiv[0]
    _tasks = d.decoding(_chrom, _ref)
    _schdl = d.create_schedule(_tasks, _ref)
    _fitness = d.get_fitness(_schdl)
    fig, gnt = plt.subplots()
    _ylim = 2 * _ref['no_machines'] * 10
    _yref = int(_ylim - (_ylim / 5))
    gnt.set_xlim(0, (1 / _fitness) + 1)
    gnt.set_ylim(_ylim)
    gnt.set_xlabel('Time per operation')
    gnt.set_ylabel('Machine')
    _size = int(_yref / _ref['no_machines'])
    _ticks = [_size + x for x in range(0, _yref, _size)]
    gnt.set_yticks(_ticks)
    gnt.set_yticklabels(list(_schdl.keys()))
    gnt.grid(False)

    for _idx, _key in enumerate(_schdl.keys()):
        for _task in _schdl[_key]:
            add_bar(gnt, _task, _size, _ticks[_idx], _colours)

    return gnt
