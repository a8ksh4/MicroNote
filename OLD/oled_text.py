from machine import Pin, I2C
import ssd1306

# https://docs.micropython.org/en/latest/esp8266/tutorial/ssd1306.html

i2c_list    = [None, None]
i2c_list[0] = I2C(0, scl=Pin(13), sda=Pin(12), freq=100_000)
i2c_list[1] = I2C(1, scl=Pin(7), sda=Pin(6), freq=100_000)

display = ssd1306.SSD1306_I2C(128, 64, i2c_list[0], 0x3c)

line_height = 10
num_lines = int(64/line_height)
TEXT_BUFFER = ['' for n in range(num_lines-1)]
TYPED_LINE = ''
LINE_LIMIT = 16


def redraw():
    global TEXT_BUFFER
    global TYPED_LINE

    display.fill(0)
    for n, line in enumerate(TEXT_BUFFER):
        display.text(line, 0, line_height*n, 1)
    display.text(TYPED_LINE, 0, line_height*(num_lines-1), 1)
    display.show()

def typed(typed_line):
    global LINE_LIMIT
    global TYPED_LINE

    if len(typed_line) > LINE_LIMIT:
        TYPED_LINE = typed_line[-LINE_LIMIT:]
    else:
        TYPED_LINE = typed_line
    print('TYPED_LINE is:', TYPED_LINE)
    redraw()

def write(new_line):
    # TODO: Rate limit, one refresh per second.
    TEXT_BUFFER[:-1] = TEXT_BUFFER[1:]
    TEXT_BUFFER[-1] = new_line
    redraw()

# display.text('Hello, World!', 0, 0, 1)
# display.show()
# display.text('Foo, Bar', 0, 8, 1)
# display.show()

def scan_i2c():
    for bus in range(0, 2):
        print("\nScanning bus %d..."%(bus))
        for addr in i2c_list[bus].scan():
            print("Found device at address %d:0x%x" %(bus, addr))
    print("Scan Done\n")