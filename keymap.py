

PINS = (7, 21, 19, 17, 15,
        4, 5, 20, 18, 16)


LAYERS = (
    # BASE
    ((1, 's'), 't', 'r', (2, 'a'), '',
     'o',      'i', 'y', (3, 'e'), ''),

    # NUMBER
    ('', '3', '2', '1', '',
     '', '6', '5', '4', ''),

    # PARENS
    ('}', '(', ')', '', '',
     '{', '[', ']', '', ''),

    # SYMBOL
    ('`', ';', '\\', '!',
     '=', '-', '?', '')
)

CHORDS = {
    ### BASE LAYER ###
    #                       'a',
    ('o', 'e'):             'b',
    ('y', 'e'):             'c',
    ('a', 'r', 't'):        'd',
    #                       'e',
    ('a', 'r'):             'f',
    ('r', 't'):             'g',
    ('i', 'e'):             'h',
    #                       'i',
    ('s', 't'):             'j',
    ('o', 'y'):             'k',
    ('e', 'y', 'i'):        'l',
    ('o', 'i', 'y'):        'm',
    ('o', 'i'):             'n',
    #                       'o',
    ('o', 'i', 'e'):        'p',
    ('s', 't', 'a'):        'q',
    #                       'r',
    #                       's',
    #                       't',
    ('y', 'i'):             'u',
    ('s', 'r'):             'v',
    ('s', 'a'):             'w',
    ('s', 't', 'r'):        'x',
    #                       'y',
    ('s', 't', 'r', 'a'):   'z',
    #
    ('o', 'i', 'y', 'e'):   ' ',
    ('y', 'a'):             '.',
    ('i', 'a'):             ',',
    ('a', 'o'):             '/',
    ('a', 'i', 'y'):        "'",
    ('t', 'i'):             '!',
    ('o', 't', 'r', 'a'):   '_tab',
    ('a', 'e'):             '_entr',
    ('s', 'e'):             '_os_ctrl',
    ('s', 'i'):             '_alt',
    ('s', 't', 'r', 'e'):   '_os_shft',
    ('r', 'e'):             '_bksp',
    ('o', 'r', 'a'):        '_esc',
}

# Sort the keys for comparison later
CHORDS = dict([(tuple(sorted(k)), v) for k, v in CHORDS.items()])
