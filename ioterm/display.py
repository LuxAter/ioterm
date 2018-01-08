import os
import math


def display_length(string):
    length = 0
    counting = True
    for char in string:
        if char == '\033':
            counting = False
        elif char == 'm' and counting is False:
            counting = True
        elif counting is True:
            length += 1
    return length


def no_attr(string, all=False):
    blocks = list()
    counting = True
    current_block = [False, '']
    for char in string:
        if char == '\033':
            counting = False
            blocks.append(current_block)
            current_block = [True, '\033']
        elif char == 'm' and counting is False:
            current_block[1] += 'm'
            counting = True
            blocks.append(current_block)
            current_block = [False, '']
        else:
            current_block[1] += char
    blocks.append(current_block)
    blocks = list(filter(lambda x: x[1], blocks))
    if all is False:
        if blocks[0][0] is True:
            blocks.pop(0)
        if blocks[-1][0] is True:
            blocks.pop(-1)
    else:
        blocks = list(filter(lambda x: x[0] is False, blocks))
    string = str()
    for block in blocks:
        string += block[1]
    return string


def truncate(string, length):
    if display_length(string) > length:
        to_del = (display_length(string) - length) + 3
        counting = True
        chars = list()
        for char in string:
            if char == '\033':
                counting = False
                chars.append((char, True))
            elif char == 'm' and counting is False:
                counting = True
                chars.append((char, True))
            elif counting is True:
                chars.append((char, False))
            else:
                chars.append((char, True))
        while to_del > 0:
            index = len(chars) - 1
            while chars[index][1] is True and index > 0:
                index -= 1
            if index == 0:
                break
            else:
                chars.pop(index)
                to_del -= 1
        string = str()
        for i in reversed(range(len(chars))):
            if chars[i][1] is False:
                chars.insert(i + 1, '.')
                chars.insert(i + 1, '.')
                chars.insert(i + 1, '.')
                break
        for item in chars:
            string += item[0]
    return string


def columnify(iterable):
    strings = [repr(x) for x in iterable]
    widest = max(len(x) for x in strings)
    padded = [x.ljust(widest) for x in strings]
    return padded


def colprint(iterable, width=-1):
    if width == -1:
        width = int(os.popen('stty size', 'r').read().split()[1])
    columns = columnify(iterable)
    colwidth = len(columns[0]) + 2
    perline = (width - 4) // colwidth
    for i, column in enumerate(columns):
        print(column, end='  ')
        if i % perline == perline - 1:
            print()
    print()


def print_aligned(string, alignment, width, end_attr=None):
    if end_attr is None:
        end_attr = str()
    if display_length(string) > width:
        return string
    if alignment == 'r':
        string = (' ' * (width - display_length(string))) + string + end_attr
    elif alignment == 'l' or alignment == '':
        string = string + end_attr + (' ' * (width - display_length(string)))
    elif alignment == 'c':
        string = (' ' * math.floor((width - display_length(string)) / 2)) + \
            string + end_attr + (' ' * math.ceil((width - display_length(string)) / 2))
    return string
