import ioterm.color as color
import ioterm.display as display

class Menu(object):
    def __init__(self):
        self.options = list()
        self.name = str()
        self.flags = {"zebra": False, "size": 0}

    def __repr__(self):
        return self.name

    #  @staticmember
    def getch(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

    def display(self, selected=-1, reset=False):
        longest = 0
        char = 0
        for el in self.options:
            longest = max(longest, len(el))
        longest = max(longest, self.flags["size"])
        char = len(repr(len(self.options)))
        if reset is True:
            print("\033[{}A".format(len(self.options) + 1), end='')
        print("\033[1m" + self.name + "\033[21m")
        for i, opt in enumerate(self.options):
            if self.flags["zebra"] is True and i % 2 != 0:
                print(color.get_color(0, True), end='')
            if i == selected:
                print("\033[7m", end='')
            print(display.print_aligned(str(i + 1), 'r', char) + '. '+ display.print_aligned(opt, 'r', longest))
            if i == selected:
                print("\033[27m", end='')
            if self.flags["zebra"] is True and i % 2 != 0:
                print(color.get_color('default', True), end='')

    def run(self, selected=-1):
        running = True
        self.display(selected)
        while running is True:
            self.display(selected, True)
            ch = self.getch()
            if ch == 'q' or ord(ch) == 13:
                running = False
            elif ch.isdigit():
                selected = int(ch) - 1
            elif ord(ch) == 27:
                ch = self.getch()
                ch = self.getch()
                if ord(ch) == 66 and selected < len(self.options) - 1:
                    selected += 1
                elif ord(ch) == 65 and selected > 0:
                    selected -= 1
        return self.options[selected]

