import color
import display
from table import Table


def main():
    tab = Table()
    data = [["\033[92mLorem ipsum dolor sit\033[39m amet, consectetur adipiscing elit.", "Vivamus facilisis odio in leo tincidunt vehicula.", "Donec vehicula odio non tortor euismod, sit amet venenatis augue ornare.", "Ut vel turpis malesuada, aliquam ipsum ac, fermentum metus.",
             "Vivamus sed purus fermentum, scelerisque ex in, scelerisque turpis."], ["Fusce euismod mauris in risus imperdiet vehicula.", "Vivamus egestas leo sed dolor facilisis, nec iaculis lectus aliquet."], ["Morbi at ex rutrum, vestibulum velit et, sollicitudin eros."], ["Vivamus quis elit non tortor eleifend tempus.", "Curabitur nec tortor congue, posuere metus facilisis, mollis risus.", "Cras in sem venenatis, maximus diam id, auctor ex.", "Mauris pretium massa a arcu euismod, a fringilla felis porta.", "Vivamus a dui scelerisque, ultrices quam non, elementum sem."], ["Pellentesque sit amet est pretium, tincidunt mi iaculis, tincidunt est.", "Quisque vel risus sed neque sodales efficitur.", "Vestibulum consequat odio nec risus lobortis blandit eget non purus."]]
    #  tab.data = [["Hello", "World", "This is a long sentance", "This is a nother", "hi", "Still going", "What about here?", "These should be trunkated", "And hopefully it works!"]]
    #  tab.data = [["Hello world, this is a long col", "Here is another long column",
                 #  "These should be more nicely trunkated as it can handdel longer sentances better"]]
    tab.data = data
    tab.flags["zebra"] = True
    #  tab.flags["title_row"] = [0, 3]
    #  tab.flags["title_col"] = [1, 4]
    tab.flags["horz_sep"] = True
    tab.flags["vert_sep"] = True
    tab.flags["corner_sep"] = True
    tab.fmt = tab.BoxFormat.UNICODE
    #  tab.fmt = tab.BoxFormat.ASCII
    tab.display()


if __name__ == "__main__":
    main()
