from machine import Pin
import time
import sys

PIN_NUMS = (25, 7)
SAFETY_PINS = [Pin(N, Pin.IN, Pin.PULL_UP) for N in PIN_NUMS]

print(f"Checking Safety Pin {PIN_NUMS}...")
time.sleep(.1)
for SAFETY_PIN in SAFETY_PINS:
    if not SAFETY_PIN.value():
        print("PIN Shorted to Ground!")
        print("Aborting loading and quitting.")
        sys.exit()