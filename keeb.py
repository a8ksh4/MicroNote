from machine import Pin
import time
from keymap import LAYERS, CHORDS

# https://docs.arduino.cc/tutorials/nano-rp2040-connect/rp2040-python-api#gpio-map
rp2040_pins = [4, 7, 5, 21, 20, 19, 18, 17, 16, 15]
pins = [Pin(n, Pin.IN, Pin.PULL_UP) for n in rp2040_pins]

#HOLD_TIME = 500
LAYER_HOLDTIME = 300
CHORD_WAITTIME = 500
ONESHOT_TIMEOUT = 2000
BASE_LAYER = 0
TICKER = 0

# Pin map to buttons:
#  1  3  5  7  9
#  0  2  4  6  8

# while True:
#     print([pin.value() for pin in pins])
#     # for n, pin in enumerate(pins):
#     #     print(pin.value())
#     time.sleep(1)
# Strategery
# First keypress starts the process
# Passing layer hold time transitions layer if it's a layer key
#    layer transition stays until layer key is released
# chord time starts when first key is pressed (or reset when layer shift is triggered)
# 
def get_pressed():
    pass

def get_next():
    global TICKER
    state = 'fresh'
    last_active = []
    ticker = 0
    layer = BASE_LAYER
    while True:
        time.sleep(0.001)
        clock = time.ticks_ms()
        active_buttons = [n for n, p  in enumerate(pins) if p.value()]

        # Idle check
        if not active_buttons and not last_active:
            continue

        # Wait for end of action button release
        if ticker == -1:
            if active_buttons:
                continue
            else:
                ticker = 0
                last_active = active_buttons

        # Start something
        if active_buttons and not last_active:
            ticker = clock
            last_active = active_buttons
            continue

        # Check HOLDTIME
        if clock - ticker > CHORD_WAITTIME:
            pressed = get_pressed(active_buttons if active_buttons else last_active)
            ticker = -1 # block until non-layer keys released
            return pressed

        # if not active_buttons:
        # if len(active_buttons) > last_active:
        #     last_active
        # # Continued Press
        # if len(last_active) ==
