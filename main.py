
import safety_pin
#import pio_junk
#from machine import Pin
#import rp2
#import time

#import os
#import myterm
#from machine import Pin, I2C
#import ssd1306
import oled_fb
import keeb

#STREAM = myterm.stream
#STREAM = oled_fb.myterm.stream
STREAM = oled_fb.scr
keeb.INJECT_FUNC = STREAM.inject

STREAM.inject('1 + 1')
STREAM.inject(b'\r')

keeb.start_timer()


# https://docs.micropython.org/en/latest/esp8266/tutorial/ssd1306.html

# i2c_list    = [None, None]
# i2c_list[0] = I2C(0, scl=Pin(13), sda=Pin(12), freq=100_000)
# i2c_list[1] = I2C(1, scl=Pin(7), sda=Pin(6), freq=100_000)

# display = ssd1306.SSD1306_I2C(128, 64, i2c_list[0], 0x3c)

# from fbconsole import FBConsole
# import os
# scr = FBConsole(display)
# os.

# KEY_BUFFER = b''
# def relayTyping(keystroke):
#     if keystroke



if __name__ == '__main__':
    print('In Main Now')
    print('and myterm:')
    #print(STREAM.read())
    #while True:
    #    print("GET NEXT:", keeb.get_next())
    

