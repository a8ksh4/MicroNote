from machine import Pin, Timer
import time
from keymap import LAYERS, CHORDS, PINS
from keys import SHIFTED, CTRLED, CODES
import collections




# https://docs.arduino.cc/tutorials/nano-rp2040-connect/rp2040-python-api#gpio-map
PINS = [Pin(p, Pin.IN, Pin.PULL_UP) for p in PINS]

#HOLD_TIME = 500
#LAYER_HOLDTIME = 300
#CHORD_WAITTIME = 500
HOLDTIME = 250
# ONESHOT_TIMEOUT = 500
BASE_LAYER = 0
TICKER = 0
EVENTS = []
PENDING_BUTTONS = set()
OS_SHIFT_PENDING = False
OS_CTRL_PENDING = False
INJECT_FUNC = None
TIMER = None
DEBUG = False
DELAYED_INPUT = [] # interface for other tools to ask for something to be typed.


# Strategery
# First keypress starts the process
# Passing layer hold time transitions layer if it's a layer key
#    layer transition stays until layer key is released
# chord time starts when first key is pressed (or reset when layer shift is triggered)
# 

def printd(foo):
    global DEBUG
    if DEBUG:
        print(foo) 

def start_timer():
    global TIMER
    TIMER = Timer(mode=Timer.PERIODIC,callback=poll_keys, freq=10)

def get_output_key(buttons, layer, tap):
    # global PINS
    global LAYERS
    global CHORDS
    #print('foo buttons:', buttons, 'layer:', layer, 'tap:', tap)

    mapped_buttons = [LAYERS[layer][b] for b in buttons]
    if len(mapped_buttons) > 1 or tap:
        # convert any hold-tap layer keys to just the (tap) key
        mapped_buttons = [b if isinstance(b, str) else b[1] for b in mapped_buttons]
        mapped_buttons = tuple(sorted(mapped_buttons))
        if len(mapped_buttons) > 1:
            result = CHORDS.get(mapped_buttons, None)
            #print("RESULT:", result)
            if isinstance(result, str):
                result = result, None
            if result is None:
                result = None, None
        else:
            result = mapped_buttons[0], None

    else:
        if isinstance(mapped_buttons[0], str):
            result = mapped_buttons[0], None
        else:
            result = None, mapped_buttons[0][0]
    
    #print(f'get output key: {buttons}, {layer}, {tap}, {result}')

    return result

def poll_keys(foo):
    #print('FOO', foo)
    global TICKER  
    global HOLDTIME
    global BASE_LAYER
    global EVENTS
    global PENDING_BUTTONS
    global PINS
    global OS_SHIFT_PENDING
    global OS_CTRL_PENDING
    global INJECT_FUNC
    global DELAYED_INPUT

    if DELAYED_INPUT:
        value = DELAYED_INPUT.pop()
        time.sleep(0.2)
        INJECT_FUNC(value)
        return

    clock = time.ticks_ms()

    current_layer = [BASE_LAYER,] + [e['layer'] for e in EVENTS if e['layer']]
    current_layer = current_layer[-1]

    buttons_pressed = [n for n, p  in enumerate(PINS) if not p.value()]
    if buttons_pressed:
        #print('Pressed:', buttons_pressed)
        pass
    # Remove events whos buttons are no longer pressed.
    for event in EVENTS:
        still_pressed = [b for b in event['buttons'] if b in buttons_pressed]
        if not still_pressed:
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

            printd(f'{(len(PENDING_BUTTONS), len(buttons_pressed), clock, TICKER, clock-TICKER)}')
            #print(PENDING_BUTTONS, current_layer, tap)
            output_key, new_layer = get_output_key(PENDING_BUTTONS, current_layer, tap)

            #print(output_key, new_layer)
            if output_key == '_set_base':
                BASE_LAYER = new_layer
                output_key, new_layer = None, None

            if output_key == '_os_shft':
                OS_SHIFT_PENDING = True
                output_key = None

            if output_key == '_os_ctrl':
                OS_CTRL_PENDING = True
                output_key = None
            
            if output_key is not None and OS_SHIFT_PENDING:
                #if not output_key.startswith('_') and len(output_key) > 1:
                if output_key in SHIFTED:
                # if len(output_key) == 1:
                    output_key = SHIFTED[output_key]
                OS_SHIFT_PENDING = False
            
            if output_key is not None and OS_CTRL_PENDING:
                if output_key in CTRLED:
                    output_key = CTRLED[output_key]
                OS_CTRL_PENDING = False

            if output_key in CODES:
                output_key = CODES[output_key]

            new_event = {'buttons': list(PENDING_BUTTONS),
                            'start_time': clock,
                            'output_key': output_key,
                            'last_output_time': 0,
                            'layer': new_layer,
                            'active': output_key is not None or new_layer is not None
                        }

            # new_event = EVENT_T(buttons=list(PENDING_BUTTONS),
            #                     start_time=clock,
            #                     output_key=output_key,
            #                     last_output_time=0,
            #                     layer=new_layer,
            #                     active=output_key is not None or new_layer is not None)
            printd('New event: {new_event}')
            #for event in EVENTS:
            #    event.active = False
            EVENTS.append(new_event)
            PENDING_BUTTONS.clear()
            TICKER = 0

    # Generate key press based on top active event.
    if EVENTS and EVENTS[-1]['active']:
        last_event = EVENTS[-1]
        if last_event['output_key'] is not None:
            INJECT_FUNC(last_event['output_key'])
            last_event['active'] = False
