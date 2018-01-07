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

def truncate(string, length):
    if display_length(string) > length:
        to_del = (display_length(string) - length) + 3
        counting = True
        chars = list()
        for char in string:
            if char == '\033':
                counting= False
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
            while chars[index][1] == True and index > 0:
                index-=1
            if index == 0:
                break
            else:
                chars.pop(index)
                to_del -=1
        string = str()
        for item in chars:
            string += item[0]
        string += "..."
    return string
