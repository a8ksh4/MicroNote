


LAYERS = (
    # BASE
    ('s', 't', 'r', 'a', '',
     'o', 'i', 'y', 'e', ''),

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
    #                       'a',
    ('o', 'e'):             'b',
    ('y', 'e'):             'c',
    ('a', 'r', 't'):        'd',
    #                       'e',
    ('a', 'r'):             'f',
    ('r', 't'):             'g',
    ('i', 'e'):             'h',
    #                       'i',
}

# Sort the keys for comparison later
CHORDS = dict([(tuple(sorted(k)), v) for k, v in CHORDS.items()])
