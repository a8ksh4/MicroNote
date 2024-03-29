SHIFTED = {
    'a': 'A',
    'b': 'B',
    'c': 'C',
    'd': 'D',
    'e': 'E',
    'f': 'F',
    'g': 'G',
    'h': 'H',
    'i': 'I',
    'j': 'J',
    'k': 'K',
    'l': 'L',
    'm': 'M',
    'n': 'N',
    'o': 'O', 
    'p': 'P',
    'q': 'Q',
    'r': 'R',
    's': 'S',
    't': 'T',
    'u': 'U',
    'v': 'V',
    'w': 'W',
    'x': 'X',
    'y': 'Y',
    'z': 'Z',
    '1': '!',
    '2': '@',
    '3': '#',
    '4': '$',
    '5': '%',
    '6': '^',
    '7': '&',
    '8': '*',
    '9': '(',
    '0': ')',
    ',': '<',
    '.': '>',
    ';': ':',
    '/': '?',
    '[': '{',
    ']': '}',
    '\\': '|',
    '-': '_',
    '=': '+',
    '`': '~',
    "'": '"',
}

# Reference: https://usermanual.wiki/buckets/88484/1582081673/XP8200_Command_Manual.pdf
CODES = {
    '_bksp': b'\b',
    '_entr': b'\r',
    '_tab': b'\t',
    '_up': b'\x1b\x5b\x41',
    '_down': b'\x1b\x5b\x42',
    '_left': b'\x1b\x5b\x44',
    '_rght': b'\x1b\x5b\x43',
    '_home': b'\x1b\x5b\x48',
    '_end': b'\x1b\x5b\x52',
}

CTRLED = {
    'a': b'\x01',
    'b': b'\x02',
    'c': b'\x03',
    'd': b'\x04',  
    

}