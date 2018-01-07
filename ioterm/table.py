import os
import color
import display
import math
from enum import Enum


class Table(object):

    class BoxFormat(Enum):
        NONE = 0
        ASCII = 1
        UNICODE = 2

    def __init__(self):
        self.data = [[]]
        self.fmt = self.BoxFormat.NONE
        self.size_data = {"rows": 0, "cols": 0,
                          "max_width": 0, "max_height": 0, "col_size": list(), "width_add": 0}
        self.flags = {"zebra": False, "vert_sep": False, "horz_sep": False, "corner_sep": False,
                      "title_row": list(), "title_col": list()}

    def update_size(self):
        self.size_data["rows"] = len(self.data)
        for row in self.data:
            self.size_data["cols"] = max(self.size_data["cols"], len(row))
        self.size_data["col_size"] = [0] * self.size_data["cols"]
        for row in self.data:
            for i, item in enumerate(row):
                self.size_data["col_size"][i] = max(
                    self.size_data["col_size"][i], len(item))

        self.size_data["max_height"], self.size_data["max_width"] = os.popen(
            'stty size', 'r').read().split()
        self.size_data["max_height"] = int(self.size_data["max_height"])
        self.size_data["max_width"] = int(self.size_data["max_width"])
        if self.fmt == self.BoxFormat.NONE or self.flags["vert_sep"] is False:
            self.size_data["width_add"] = self.size_data["cols"] - 1
        else:
            self.size_data["width_add"] = (
                3 * (self.size_data["cols"] - 1)) + 4
        if sum(self.size_data["col_size"]) + self.size_data["width_add"] > self.size_data["max_width"]:
            norm = [float(i) / (sum(self.size_data["col_size"]) +
                                self.size_data["width_add"]) for i in self.size_data["col_size"]]
            self.size_data["col_size"] = [
                int(math.floor(self.size_data["max_width"] * i)) for i in norm]
            while sum(self.size_data["col_size"]) + self.size_data["width_add"] > self.size_data["max_width"]:
                self.size_data["col_size"][-1] -= 1

    def vert(self, pos=1):
        ch = '|'
        if self.fmt == self.BoxFormat.NONE or self.flags["vert_sep"] is False:
            if pos == 1:
                print(' ', end='')
            if pos == 2:
                print()
            return
        elif self.fmt == self.BoxFormat.ASCII:
            ch = '|'
        elif self.fmt == self.BoxFormat.UNICODE:
            ch = '\u2502'
        if pos == 0:
            print('{} '.format(ch), end='')
        elif pos == 1:
            print(' {} '.format(ch), end='')
        elif pos == 2:
            print(' {}'.format(ch))

    def horz(self, pos=1):
        ch = '-'
        if self.fmt == self.BoxFormat.NONE or self.flags["horz_sep"] is False:
            return
        elif self.fmt == self.BoxFormat.ASCII:
            ch = '-'
        elif self.fmt == self.BoxFormat.UNICODE:
            ch = '\u2500'
        has_vert = self.flags["vert_sep"] and self.fmt != self.BoxFormat.NONE
        if has_vert is False or self.flags["corner_sep"] is False:
            print(
                ch * (sum(self.size_data["col_size"]) + self.size_data["width_add"]))
        else:
            self.corner((pos * 3))
            for i, item in enumerate(self.size_data["col_size"]):
                print(ch * (item + 2), end='')
                if i != len(self.size_data["col_size"]) -1:
                    self.corner((pos * 3) + 1)
            self.corner((pos * 3) + 2)

    def corner(self, pos=4):
        ch ='+'
        if self.fmt == self.BoxFormat.NONE:
            ch = ''
        elif self.fmt == self.BoxFormat.ASCII:
            ch = '+'
        elif self.fmt == self.BoxFormat.UNICODE:
            if pos == 0:
                ch = '\u250C'
            elif pos == 1:
                ch = '\u252C'
            elif pos == 2:
                ch = '\u2510'
            elif pos == 3:
                ch = '\u251C'
            elif pos == 4:
                ch = '\u253C'
            elif pos == 5:
                ch = '\u2524'
            elif pos == 6:
                ch = '\u2514'
            elif pos == 7:
                ch = '\u2534'
            elif pos == 8:
                ch = '\u2518'
        print(ch, end='')


    def display(self):
        self.update_size()
        self.horz(0)
        for j, row in enumerate(self.data):
            if self.flags["zebra"] is True and j % 2 != 0:
                print(color.get_color(0, True), end='')
            self.vert(0)
            for i, item in enumerate(row):
                item = display.truncate(item, self.size_data["col_size"][i])
                if i in self.flags["title_col"] or j in self.flags["title_row"]:
                    print("\033[1m", end='')
                print(item, end='')
                if len(item) < self.size_data["col_size"][i]:
                    print(
                        ' ' * (self.size_data["col_size"][i] - len(item)), end='')
                if i in self.flags["title_col"] or j in self.flags["title_row"]:
                    print("\033[21m", end='')
                if i != self.size_data["cols"] - 1:
                    self.vert()
            for i in range(len(row), self.size_data["cols"]):
                print(' ' * self.size_data["col_size"][i], end='')
                if i != self.size_data["cols"] - 1:
                    self.vert()
            self.vert(2)
            if self.flags["zebra"] is True and j % 2 != 0:
                print(color.get_color("default", True), end='')
            if j != len(self.data) - 1:
                self.horz()
        self.horz(2)
