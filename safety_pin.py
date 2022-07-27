from machine import Pin
import time
import sys

PIN_NUM = 25
SAFETY_PIN = Pin(PIN_NUM, Pin.IN, Pin.PULL_UP)

print(f"Checking Safety Pin {PIN_NUM}...")
time.sleep(.1)
if not SAFETY_PIN.value():
    print("PIN Shorted to Ground!")
    print("Aborting loading and quitting.")
    sys.exit()