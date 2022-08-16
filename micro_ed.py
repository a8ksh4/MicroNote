
import os

PROMPT = ':'
LINE_DELIM = '\n'
HELP = False
DELAYED_INPUT = None

def ed(fname=None, prompt=PROMPT):
    global HELP
    global DELAYED_INPUT
    if fname is None or not os.path.exists(fname):
        lines = []
        fsize = 0
    else:
        fsize = os.stat(fname)[6]
        with open(fname, 'r') as f:
            lines = f.readlines()
            lines = [l.rstrp() for l in lines]

    print(fsize)
    mode = 'cmd'
    err = None
    current_line = 0
    while True:
        if mode == 'cmd':
            txt = input(prompt)
            mode = txt[-1]
            cfg = txt[:-1]
            thx = ''
             
        elif mode == 'H':
            HELP = not HELP
            mode = 'cmd'

        elif mode.endswith('c'):
            mode = 'a'
            DELAYED_INPUT.append(lines[current_line])

        elif mode.endswith('a'):
            txt = input()
            if txt == '.':
                mode = 'cmd'
            else:
                lines.append(txt)

        elif mode.endswith('p'):
            mode = 'cmd'
            for line in lines:
                print(line)
        
        elif mode.endswith('n'):
            mode = 'cmd'
            for n, line in enumerate(lines):
                print(n, line)

        elif mode == 'w':
            mode = 'cmd'
            if fname is None:
                err = "No Filename"
            else:
                with open(fname, 'w') as f:
                    f.writelines(lines)

        elif mode == 'q':
            break

        else:
            err = "Unknown command"
        if err is not None:
            print('?')
            if HELP:
                print(err)
            mode = 'cmd'
            err = None
            
