# Micro Note
It's a:
* Pocket Notetaker
* Calclator
* MicroPython Repl
* SSH Client
* And much more!

## Hardware
* **System Board** - Pi Pico, Pi Pico W, Arduino Nano RP2040 Connect, other RP2040 boards, or probably any other board that runs micropython. 
* **Charger** - USB 1S Li-Ion Charger board.  E.g. https://www.amazon.com/gp/product/B071RG4YWM/
* **Battery** - Any single Lithium Ion cell, 18650, pouch, whatever. 
* **Power Switch** - 
* **Boost Board** - * *If your chosen system board operate down to ~3.3v as the battery discharges, a boost regulator should be employed to keep voltage up to 5v.
* **Keyboard** - The design example uses Artsey.io chording layout.  Should be able to wire up any keybord layout and modify the keymaps.
* **Display** - Development is being done on an SSD1306 for simplicity, but modules should be added other displays.  E.g. the Sharp Memory Display (https://www.adafruit.com/product/4694) would be very cool.
  * https://forum.micropython.org/viewtopic.php?f=15&t=11551
* 

## Planned Functions
* Editor with local storage
* Network file sync
* SSH
* Interactve repl
* Session and State persestency - define new functions and have them available next time you power on.  Might want to make all critical system variables, functions, modules, etc use * *_name* * to avoid conficts. I'm not sure Micropython supports separate namespaces for exec().  Either tag stuff to be kept or just write global() to disk periodically...

## Modules
* "keeb.py" for user input - Depends on "keymap.py" for the keyboard layout, layers, and chords.  
* "wifi.py" for network connectivity (if your board supports it)
* "
