
import safety_pin
import pio_junk
from machine import Pin
import rp2
import time

COUNT = 0

def initPinsAsIn(direction=Pin.PULL_UP):
    for n in range(32):
        try:
            Pin(n, Pin.IN, direction)
        except:
            print("Couldn't initialize pin:", n)


def printFromGet(sm):
    global COUNT
    out = sm.get()
    print(f'{COUNT} - {out:>032b}')
    COUNT += 1


if __name__ == '__main__':
    print('In Main Now')
    
    initPinsAsIn()

    sm = rp2.StateMachine(0, pio_junk.irq_pins_changes,
                            freq=2000, in_base=Pin(0))
    sm.irq(printFromGet, 0)

    sm.active(1)
    for n in range(10):
        out = sm.get()
        print(f'{n}, {out:>032b}')
    sm.active(0)
