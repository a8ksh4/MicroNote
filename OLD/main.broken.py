from pio_junk import blink_1hz
import wifi
#import oled_text as oled
import oled_fb as oled
import time
#import repl
#import keeb
#import gc
#from io import StringIO
#from contextlib import redirect_stdout

#import io
import os
import _thread
from machine import Pin
import rp2
import oled_text as oled
import pio_junk


oled.write("Hello World!")
print("Hello World!")

# Plain Blink
# sm = rp2.StateMachine(0, blink, freq=2000, set_base=Pin(6))
# sm.active(1)
# time.sleep(3)
# sm.active(0)

# Blink 1Hz IRQ
# Create the StateMachine with the blink_1hz program, outputting on Pin(25).
#sm = rp2.StateMachine(0, blink_1hz, freq=2000, set_base=Pin(6))
# Set the IRQ handler to print the millisecond timestamp.
#sm.irq(lambda p: print(time.ticks_ms()))
# Start the StateMachine.
#sm.active(1)

p2 = Pin(2, Pin.IN, Pin.PULL_UP)
p2.irq(lambda pin: print("IRQ with flags:", pin.irq().flags()), Pin.IRQ_FALLING)


# Read Keys
sm = rp2.StateMachine(0, pio_junk.query_all_pins, freq=2000, set_base=Pin(15))
sm.irq(lambda p: print("bar", time.ticks_ms()), 0)
sm.irq(lambda p: print("foo", time.ticks_ms()), 1)
sm.active(1)

