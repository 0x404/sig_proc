#!/usr/bin/env python
# encoding: utf-8

# Jakub Młokosiewicz, 2015

from mysignalslib import Wave
from matplotlib import pyplot
from math import pi, floor, ceil

def inf_iter(obj):
    while True:
        for x in obj:
            yield x

def set_x_ticks(plot, min_x, max_x, density=None):
    # now it works only for min_x == 0
    density_vals = ('very tight', 'tight', 'normal', 'loose', None)
    if density not in density_vals:
        raise ValueError('Possible values for density: ' + ', '.join(density_vals) + ' (auto)')
    if density is None:
        diff = (max_x - min_x) / pi
        if diff <= 2:
            density = 'very tight'
        elif diff <= 5:
            density = 'tight'
        elif diff <= 10:
            density = 'normal'
        else:
            density = 'loose'
    x_ticks = [0]
    x_labels = ['']
    max_x_pis = max_x / pi
    max_x_full_pis = ceil(max_x_pis)
    too_much = max_x_full_pis - max_x_pis
    if density == 'very tight':
        for i in range(max_x_full_pis):
            x_ticks += [
                (i + 1/8) * pi,
                (i + 1/4) * pi,
                (i + 3/8) * pi,
                (i + 1/2) * pi,
                (i + 5/8) * pi,
                (i + 3/4) * pi,
                (i + 7/8) * pi,
                (i + 1) * pi]
            x_labels += [
                '$\\frac{%i}{8}\\pi$' % (i*8 + 1),
                '$\\frac{%i}{4}\\pi$' % (i*4 + 1),
                '$\\frac{%i}{8}\\pi$' % (i*8 + 3),
                '$\\frac{%i}{2}\\pi$' % (i*2 + 1),
                '$\\frac{%i}{8}\\pi$' % (i*8 + 5),
                '$\\frac{%i}{4}\\pi$' % (i*4 + 3),
                '$\\frac{%i}{8}\\pi$' % (i*8 + 7),
                '$%i\\pi$' % (i + 1)
            ]
        for x in range(1, 9):
            if too_much < x / 8:
                break
            x_ticks.pop()
            x_labels.pop()

    elif density == 'tight':
        for i in range(max_x_full_pis):
            x_ticks += [
                (i + 1/4) * pi,
                (i + 1/2) * pi,
                (i + 3/4) * pi,
                (i + 1) * pi]
            x_labels += [
                '$\\frac{%i}{4}\\pi$' % (i*4 + 1),
                '$\\frac{%i}{2}\\pi$' % (i*2 + 1),
                '$\\frac{%i}{4}\\pi$' % (i*4 + 3),
                '$%i\\pi$' % (i + 1)
            ]
    elif density == 'normal':
        for i in range(max_x_full_pis):
            x_ticks += [
                (i + 1/2) * pi,
                (i + 1) * pi]
            x_labels += [
                '$\\frac{%i}{2}\\pi$' % (i*2 + 1),
                '$%i\\pi$' % (i + 1)
            ]
    else:
        for i in range(max_x_full_pis):
            x_ticks += [
                (i + 1) * pi]
            x_labels += [
                '$%i\\pi$' % (i + 1)
            ]
    plot.set_xticks(x_ticks)
    plot.set_xticklabels(x_labels)

def multiplot(*subplots, others=[], x_range=None):
    num_rows = len(subplots) + len(others)
    grid_size = (num_rows, 1)
    x_range = x_range or Wave.x_range(*sum(subplots, []))
    y_range = Wave.y_range(*sum(subplots, []), spacing=(1, 1))
    colors = inf_iter(['turquoise', 'hotpink', 'dodgerblue', 'slateblue', 'darkorchid'])
    for index, subplot in enumerate(subplots):
        plot = pyplot.subplot2grid(grid_size, (index, 0))
        pyplot.hold(True)
        pyplot.grid(True)
        for wave in subplot:
            wave.plot(next(colors))
        pyplot.ylim(y_range)
        pyplot.xlim(x_range)
        set_x_ticks(plot, *x_range)
        pyplot.locator_params(axis='y', nbins=20)
        pyplot.tick_params(axis='y', labelsize=9)
        pyplot.tick_params(axis='x', labelsize=13)
        pyplot.legend(ncol=3, loc='upper center', bbox_to_anchor=(0.5, 1.15))
    for index, other in enumerate(others):
        plot = pyplot.subplot2grid(grid_size, (len(subplots) + index, 0))
        pyplot.grid(True)
        other.plot(next(colors))
        pyplot.tick_params(axis='y', labelsize=9)
        pyplot.tick_params(axis='x', labelsize=9)
        pyplot.legend(ncol=3, loc='upper center', bbox_to_anchor=(0.5, 1.15))
    pyplot.tight_layout()
    pyplot.subplots_adjust(top=0.9, hspace=0.3)