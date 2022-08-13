from machine import Pin, Timer
import time
from keymap import LAYERS, CHORDS, PINS
from keys import SHIFTED, CTRLED, ASCII_CODES
import collections


# https://docs.arduino.cc/tutorials/nano-rp2040-connect/rp2040-python-api#gpio-map
PINS = [Pin(p, Pin.IN, Pin.PULL_UP) for p in PINS]
HOLDTIME = 1000
ONESHOT_TIMEOUT = 2000
BASE_LAYER = 0
TICKER = 0
EVENTS = []
PENDING_BUTTONS = set()
OS_SHIFT_PENDING = False
OS_CTRL_PENDING = False
# CRAPPY_MUTEX = False

EVENT_FIELDS = ('buttons', 'start_time', 'output_key', 'layer', 'active', 'last_output_time')
EVENT_VALS = [None for f in EVENT_FIELDS]
EVENTS_POOL = [dict(zip(EVENT_FIELDS, EVENT_VALS)) for n in range(10)]
EVENTS = []


def activate(callback_func):
    global CALLBACK
    global TIMER
    TIMER = None
    CALLBACK = callback_func
    # TIMER = Timer(mode=Timer.PERIODIC,callback=callback_func)
    #TIMER = Timer(mode=Timer.PERIODIC,
                    # period=100,
                    # callback=get_next)

def get_output_key(buttons, layer, tap):
    # global PINS
    global LAYERS
    global CHORDS

    print('in get output')
    mapped_buttons = [LAYERS[layer][b] for b in buttons]
    if len(mapped_buttons) > 1 or tap:
        # convert any hold-tap layer keys to just the (tap) key
        mapped_buttons = [b if isinstance(b, str) else b[1] for b in mapped_buttons]
        mapped_buttons = tuple(sorted(mapped_buttons))
        if len(mapped_buttons) > 1:
            result = CHORDS.get(mapped_buttons, None), None
        else:
            result = mapped_buttons[0], None

    else:
        if isinstance(mapped_buttons[0], str):
            result = mapped_buttons[0], None
        else:
            result = None, mapped_buttons[0][0]
    
    print('get output key', buttons, layer, tap, result)

    return result

def get_next():
    global TICKER  
    global HOLDTIME
    global BASE_LAYER
    global EVENTS
    global PENDING_BUTTONS
    global PINS
    global OS_SHIFT_PENDING
    global OS_CTRL_PENDING
    # global CRAPPY_MUTEX
    global CALLBACK

    # if CRAPPY_MUTEX:
    #     return

    # CRAPPY_MUTEX = True

    # Un-looped this, expecting to call using timer callback
    clock = time.ticks_ms()

    current_layer = [BASE_LAYER,] + [e.layer for e in EVENTS if e.layer]
    current_layer = current_layer[-1]

    buttons_pressed = [n for n, p  in enumerate(PINS) if not p.value()]
    if buttons_pressed:
        #print('Pressed:', buttons_pressed)
        pass
    # Remove events whos buttons are no longer pressed.
    for event in EVENTS:
        still_pressed = [b for b in event['buttons'] if b in buttons_pressed]
        if not still_pressed:
            EVENTS_POOL.append(event)
    # for event in EVENTS_POOL:
    #     if event in EVENTS:
            EVENTS.remove(event)

    # Remove buttons from buttons_pressed if associated with an event
    all_event_butons = sum([e['buttons'] for e in EVENTS], [])
    #print('all event buttons:', all_event_butons)
    buttons_pressed = [b for b in buttons_pressed if b not in all_event_butons]
    # TODO: mark events inactive if not all of their original buttons are still pressed.

    # Move buttons_pressed to pending
    PENDING_BUTTONS.update(buttons_pressed)
    # At this point, pending buttons is only buttons pressed that have not been associated with an event. 

    if PENDING_BUTTONS:
        if not TICKER:
            TICKER = clock
        #print('Pending:', PENDING_BUTTONS)

        # Check conditions for new event - Keys starting to be released or hold_time exceeded
        # TODO: maybe separate hold times for layer stuff vs chords. 
        if ( len(PENDING_BUTTONS) > len(buttons_pressed) 
                or clock - TICKER > HOLDTIME ):
            tap =  clock - TICKER < HOLDTIME

            print(len(PENDING_BUTTONS), len(buttons_pressed), clock, TICKER, clock-TICKER)
            output_key, new_layer = get_output_key(PENDING_BUTTONS, current_layer, tap)

            if output_key == '_os_shft':
                OS_SHIFT_PENDING = True
                output_key = None
            elif output_key == '_os_ctrl':
                OS_CTRL_PENDING = True
                OS_SHIFT_PENDING = False
                output_key = None
            elif output_key.startswith('_') and len(output_key) > 1: # it's not just "_"
                output_key = ASCII_CODES[output_key]
            
            elif output_key is not None and OS_SHIFT_PENDING:
                #if not output_key.startswith('_') and len(output_key) > 1:
                if len(output_key) == 1:
                    output_key = SHIFTED[output_key]
                OS_SHIFT_PENDING = False

            elif output_key is not None and OS_CTRL_PENDING:
                if len(output_key) == 1:
                    output_key = CTRLED[output_key]
                OS_CTRL_PENDING = False

            new_event = EVENTS_POOL.pop()
            new_event['buttons'] = list(PENDING_BUTTONS)
            new_event['start_time'] = clock
            new_event['output_key'] = output_key
            new_event['layer'] = new_layer,
            new_event['active'] = output_key is not None or new_layer is not None
            # new_event = EVENT_T(buttons=list(PENDING_BUTTONS),
            #                     start_time=clock,
            #                     output_key=output_key,
            #                     last_output_time=0,
            #                     layer=new_layer,
            #                     active=output_key is not None or new_layer is not None)
            print('New event:', new_event)
            #for event in EVENTS:
            #    event.active = False
            EVENTS.append(new_event)
            PENDING_BUTTONS.clear()
            TICKER = 0

    # Generate key press based on top active event.
    if EVENTS and EVENTS[-1].active:
        last_event = EVENTS[-1]
        last_event.active = False
        if last_event['output_key'] is not None:  
            CALLBACK(last_event.output_key)
    
    CRAPPY_MUTEX = False
 