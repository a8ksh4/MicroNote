from machine import Pin, I2C
import ssd1306
from fbconsole import FBConsole
import os
#import myterm

# https://docs.micropython.org/en/latest/esp8266/tutorial/ssd1306.html

i2c_list    = [None, None]
i2c_list[0] = I2C(0, scl=Pin(13), sda=Pin(12), freq=100_000)
i2c_list[1] = I2C(1, scl=Pin(7), sda=Pin(6), freq=100_000)

display = ssd1306.SSD1306_I2C(128, 64, i2c_list[0], 0x3c)


scr = FBConsole(display) #, readobj=myterm.stream)
os.dupterm(scr)



# def redraw():
#     pass

# def typed(typed_line):
#     pass

# def write(new_line):
#     # TODO: Rate limit, one refresh per second.
#     print(new_line)

# display.text('Hello, World!', 0, 0, 1)
# display.show()
# display.text('Foo, Bar', 0, 8, 1)
# display.show()

# def scan_i2c():
#     for bus in range(0, 2):
#         print("\nScanning bus %d..."%(bus))
#         for addr in i2c_list[bus].scan():
#             print("Found device at address %d:0x%x" %(bus, addr))
#     print("Scan Done\n")