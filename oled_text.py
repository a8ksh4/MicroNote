from machine import Pin, I2C
import ssd1306

# https://docs.micropython.org/en/latest/esp8266/tutorial/ssd1306.html

i2c_list    = [None, None]
i2c_list[0] = I2C(0, scl=Pin(13), sda=Pin(12), freq=100_000)
i2c_list[1] = I2C(1, scl=Pin(7), sda=Pin(6), freq=100_000)

display = ssd1306.SSD1306_I2C(128, 64, i2c_list[0], 0x3c)

line_height = 10
num_lines = int(64/line_height)
text_buffer = ['' for n in range(num_lines)]

def write(new_line):
    # TODO: Rate limit, one refresh per second.
    text_buffer[:-1] = text_buffer[1:]
    text_buffer[-1] = new_line
    display.fill(0)
    for n, line in enumerate(text_buffer):
        display.text(line, 0, line_height*n, 1)
    display.show()

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