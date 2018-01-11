import ioterm.color as color

import math
import numpy as np


def print_char(fill, a, b):
    string = color.get_color(a)
    if fill != 8:
        string += color.get_color(b, True)
    if fill == 8:
        string += '\u2588'
    elif fill == 7:
        string += '\u2589'
    elif fill == 6:
        string += '\u258A'
    elif fill == 5:
        string += '\u258B'
    elif fill == 4:
        string += '\u258C'
    elif fill == 3:
        string += '\u258D'
    elif fill == 2:
        string += '\u258E'
    elif fill == 1:
        string += '\u258F'
    string += color.get_color('default')
    if fill != 8:
        string += color.get_color('default', True)
    return string


def print_bar_single(percent, width, write_percent, colors):
    perc = "%{:4.3}".format(percent)
    if percent > 1:
        percent /= 100.0
    chars = [''] * width
    switch = 0
    for i, v in zip(range(width), np.arange(0.0, 1.0, (1.0 / width))):
        if v >= percent and switch is 0:
            chars[i] += color.get_color(colors[0]) + \
                color.get_color(colors[1], True)
            switch = 1
        if i < len(perc) and write_percent is True:
            chars[i] += perc[i]
            if switch == 1:
                switch = 2
        elif switch == 1:
            switch = 2
            dec = (percent * width) % 1
            if dec < 0.125:
                chars[i] += ' '
            elif dec < 0.25:
                chars[i] += '\u258f'
            elif dec < 0.375:
                chars[i] += '\u258e'
            elif dec < 0.5:
                chars[i] += '\u258d'
            elif dec < 0.625:
                chars[i] += '\u258c'
            elif dec < 0.75:
                chars[i] += '\u258b'
            elif dec < 0.875:
                chars[i] += '\u258a'
            elif dec < 1.0:
                chars[i] += '\u2589'
        else:
            chars[i] += ' '
    string = color.get_color(colors[0], True)
    string += color.get_color(colors[1])
    string += ''.join(chars)
    string += color.get_color('default')
    string += color.get_color('default', True)
    return string


def print_bar_multi(percents, width, write_percent, colors):
    tmp = colors[-1]
    colors = [x for _,x in sorted(zip(percents,colors[:-1]))]
    colors.append(tmp)
    percents = sorted(percents)
    perc = ["%{:4.1f}".format(x) for x in percents]
    percents = [x / 100 if x > 1 else x for x in percents]
    chars = [''] * width
    switch = 0
    index = 0
    ch_index = 0
    for i, v in zip(range(width), np.arange(0.0, 1.0, (1.0 / width))):
        if index < len(percents) and v >= percents[index] and switch is 0:
            chars[i] += color.get_color(colors[index]) + \
                color.get_color(colors[index + 1], True)
            switch = 1
        if index < len(perc) and ch_index < len(perc[index]) and write_percent is True:
            if switch == 1:
                dec = (percents[index] * width) % 1
                if dec >= 0.5:
                    chars[i] += color.get_color(colors[-1])
                    chars[i] += perc[index][ch_index]
                elif dec < 0.125:
                    chars[i] += ' '
                elif dec < 0.25:
                    chars[i] += '\u258f'
                elif dec < 0.375:
                    chars[i] += '\u258e'
                elif dec < 0.5:
                    chars[i] += '\u258d'
                switch = 0
                index += 1
                ch_index = 0
            else:
                chars[i] += color.get_color(colors[-1])
                chars[i] += perc[index][ch_index]
                ch_index += 1
        elif switch == 1:
            switch = 2
            dec = (percents[index] * width) % 1
            if dec < 0.125:
                chars[i] += ' '
            elif dec < 0.25:
                chars[i] += '\u258f'
            elif dec < 0.375:
                chars[i] += '\u258e'
            elif dec < 0.5:
                chars[i] += '\u258d'
            elif dec < 0.625:
                chars[i] += '\u258c'
            elif dec < 0.75:
                chars[i] += '\u258b'
            elif dec < 0.875:
                chars[i] += '\u258a'
            elif dec < 1.0:
                chars[i] += '\u2589'
            index += 1
            switch = 0
            ch_index = 0
        else:
            chars[i] += ' '
    string = color.get_color(colors[0], True)
    string += color.get_color(colors[-1])
    string += ''.join(chars)
    string += color.get_color('default')
    string += color.get_color('default', True)
    return string


def print_bar(percent, width=79, write_percent=True, colors=["green", "black"]):
    if isinstance(percent, float):
        return print_bar_single(percent, width, write_percent, colors)
    elif isinstance(percent, list):
        return print_bar_multi(percent, width, write_percent, colors)
