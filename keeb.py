from machine import Pin
import time
from keymap import LAYERS, CHORDS
import collections

EVENT_T = collections.namedtuple('buttons', 
                                'start_time', 
                                'output_key',
                                'last_output_time',
                                'layer')


# https://docs.arduino.cc/tutorials/nano-rp2040-connect/rp2040-python-api#gpio-map
rp2040_pins = [4, 7, 5, 21, 20, 19, 18, 17, 16, 15]
pins = [Pin(n, Pin.IN, Pin.PULL_UP) for n in rp2040_pins]

#HOLD_TIME = 500
#LAYER_HOLDTIME = 300
#CHORD_WAITTIME = 500
HOLDTIME = 500
ONESHOT_TIMEOUT = 2000
BASE_LAYER = 0
TICKER = 0
EVENTS = []
PENDING_BUTTONS = set()
# (keys, start_time, output key, last_output_time)
# (pins, start_time, output_key, last_output_time)

# Pin map to buttons:
#  1  3  5  7  9
#  0  2  4  6  8


# Strategery
# First keypress starts the process
# Passing layer hold time transitions layer if it's a layer key
#    layer transition stays until layer key is released
# chord time starts when first key is pressed (or reset when layer shift is triggered)
# 
def get_output_key(buttons, layer):
    pass

def get_next():
    global TICKER
    global HOLDTIME
    global BASE_LAYER
    global EVENTS
    global PENDING_BUTTONS

    while True:
        time.sleep(0.001)
        clock = time.ticks_ms()

        current_layer = [BASE_LAYER,] + [e.layer for e in EVENTS if e.layer]
        current_layer = current_layer[-1]

        buttons_pressed = [n for n, p  in enumerate(pins) if p.value()]
        new_event = False

        # Remove events whos buttons are no longer pressed.
        for event in EVENTS:
            still_pressed = [b for b in event.buttons if b in buttons_pressed]
            if not still_pressed:
                EVENTS.remove(event)

        # Remove buttons from buttons_pressed if associated with an event
        all_event_butons = sum([e.buttons for e in EVENTS])
        buttons_pressed = [b for b in buttons_pressed if b not in all_event_butons]
        # TODO: mark events inactive if not all of their original buttons are still pressed.

        # Move buttons_pressed to pending
        PENDING_BUTTONS.update(buttons_pressed)
        # At this point, pending buttons is only buttons pressed that have not been associated with an event. 

        if PENDING_BUTTONS:
            if not TICKER:
                TICKER = clock

            # Check conditions for new event - Keys starting to be released or hold_time exceeded
            # TODO: maybe separate hold times for layer stuff vs chords. 
            if ( len(PENDING_BUTTONS) > len(buttons_pressed) 
                    or clock - TICKER > HOLDTIME ):
                output_key, new_layer = get_output_key(buttons, curernt_layer)
                new_event = EVENT_T(buttons=list(PENDING_BUTTONS),
                                    start_time=clock,
                                    output_key=output_key,
                                    last_output_time=0,
                                    layer=new_layer)

        if EVENTS:
            last_event = EVENTS[-1]
            return_key = last_event.outpu
