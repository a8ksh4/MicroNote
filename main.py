import wifi
import oled_text as oled
import time
#import repl
import keeb
import gc
from io import StringIO
#from contextlib import redirect_stdout

import io
import os

class DUP(io.IOBase):

    def __init__(self, s):
        self.s = s

    def write(self, data):
        self.s += data
        return len(data)

    def readinto(self, data):
        return 0


WIFI_NET = 'foo'
WIFI_PASS = 'bar'

# using default address 0x3C
# i2c = I2C(sda=Pin(4), scl=Pin(5))
# display = ssd1306.SSD1306_I2C(128, 64, i2c)

# display.text('Hello, World!', 0, 0, 1)
# display.show()

if __name__ == '__main__':
    oled.write('Running.')
    #time.sleep(1)
    oled.write('Hello world!')
    #time.sleep(1)
    oled.write(f'Pairing wifi:')
    oled.write(f'    {WIFI_NET}')
    status = wifi.join_network(WIFI_NET, WIFI_PASS)
    oled.write(f'Pairing status:')
    oled.write(f'    {status}')

    oled.write(f'Enter the keys...')
    char_buffer = []
    new_stdout = StringIO()

    while True:
        pressed = keeb.get_next()

        if pressed is None:
            continue
        print("Main received key:", pressed)

        if pressed == "_bspc":
            if char_buffer:
                char_buffer.pop()
        elif pressed in ('_ctrl', '_alt', '_tab', '_del'):
            print('Skipped key:', pressed)
        elif pressed == "_entr":
            with redirect_stdout(new_stdout):
                exec_string = ''.join(char_buffer)
            s = new_stdout.getvalue()

            oled.write(exec_string)
            try:
                output = exec(exec_string)
            except Exception as e:
                output = str(e)
            #for line in output:
            #    oled.write(line)
            oled.write(str(output))
            char_buffer.clear()
        else:
            char_buffer.append(pressed)
        oled.typed(''.join(char_buffer)) 
        gc.collect()


