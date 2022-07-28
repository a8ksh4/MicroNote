from machine import Pin
import rp2
from rp2 import PIO
import time
from keymap import LAYERS, CHORDS, PINS
from keys import SHIFTED
import collections

# https://docs.arduino.cc/tutorials/nano-rp2040-connect/rp2040-python-api#gpio-map
#PINS = [Pin(p, Pin.IN, Pin.PULL_UP) for p in PINS]

#HOLD_TIME = 500
#LAYER_HOLDTIME = 300
#CHORD_WAITTIME = 500
HOLDTIME = 1000
ONESHOT_TIMEOUT = 2000
BASE_LAYER = 0
TICKER = 0
EVENTS = []
PENDING_BUTTONS = set()
OS_SHIFT_PENDING = False

EVENT_T = collections.namedtuple("Event", ('buttons', 
                                'start_time', 
                                'output_key',
                                'last_output_time',
                                'layer',
                                'active'))

@rp2.asm_pio( set_init=[PIO.IN_HIGH]*32 )
def irq_pins_changes():
    mov(y, pins)
    #in_(y, 32)
    mov(isr, y)
    push()

    wrap_target()
    label("read loop")
    mov(x, pins)

    jmp(x_not_y, "exit read loop")
    jmp("read loop")
    label("exit read loop")
    
    mov(isr, x)
    mov(y, x)
    push()
    irq(1)

    wrap()


# Strategery
# First keypress starts the process
# Passing layer hold time transitions layer if it's a layer key
#    layer transition stays until layer key is released
# chord time starts when first key is pressed (or reset when layer shift is triggered)
# 
def get_output_key(buttons, layer, tap):
    # global PINS
    global LAYERS
    global CHORDS

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

def initInputPins(direction=Pin.PULL_UP):
    for n in range(32):
        try:
            Pin(n, Pin.IN, direction)
        except:
            print("Couldn't initialize pin:", n)

def activate(callback_func):
    global SM
    global CALLBACK 
    global PINS_START
    CALLBACK = callback_func
    initInputPins()
    rp2.PIO(0).irq(process_next)
    SM = rp2.StateMachine(0, irq_pins_changes,
                            freq=2000, in_base=Pin(0))
    #SM.irq(process_next, 0)
    SM.active(1)
    PINS_START = SM.get()
    print(f'Initial Pin States: {PINS_START::>032b}')

def pins_to_buttons(pins_next):
    global PINS_START
    same = PINS_START ^ pins_next
    pins = [n for n in range(32) if same & 2**n]
    return(pins)

def process_next(sm):
    global CALLBACK
    pin_states = sm.state_machine(0).get()
    buttons_pressed = pins_to_buttons(pin_states)
    CALLBACK(buttons_pressed)


def get_next():
    global TICKER  
    global HOLDTIME
    global BASE_LAYER
    global EVENTS
    global PENDING_BUTTONS
    global PINS
    global OS_SHIFT_PENDING

    while True:
        time.sleep(.001)
        clock = time.ticks_ms()

        current_layer = [BASE_LAYER,] + [e.layer for e in EVENTS if e.layer]
        current_layer = current_layer[-1]

        buttons_pressed = [n for n, p  in enumerate(PINS) if not p.value()]
        if buttons_pressed:
            #print('Pressed:', buttons_pressed)
            pass
        # Remove events whos buttons are no longer pressed.
        for event in EVENTS:
            still_pressed = [b for b in event.buttons if b in buttons_pressed]
            if not still_pressed:
                EVENTS.remove(event)

        # Remove buttons from buttons_pressed if associated with an event
        all_event_butons = sum([e.buttons for e in EVENTS], [])
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
                
                if output_key is not None and OS_SHIFT_PENDING:
                    #if not output_key.startswith('_') and len(output_key) > 1:
                    if len(output_key) == 1:
                        output_key = SHIFTED[output_key]
                    OS_SHIFT_PENDING = False

                new_event = EVENT_T(buttons=list(PENDING_BUTTONS),
                                    start_time=clock,
                                    output_key=output_key,
                                    last_output_time=0,
                                    layer=new_layer,
                                    active=output_key is not None or new_layer is not None)
                print('New event:', new_event)
                #for event in EVENTS:
                #    event.active = False
                EVENTS.append(new_event)
                PENDING_BUTTONS.clear()
                TICKER = 0

        # Generate key press based on top active event.
        if EVENTS and EVENTS[-1].active:
            last_event = EVENTS[-1]
            return(last_event.output_key)
 