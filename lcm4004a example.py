import time
from machine import Pin

# D4 = Pin(14, Pin.OUT)
# D5 = Pin(15, Pin.OUT)
# D6 = Pin(16, Pin.OUT)
# D7 = Pin(17, Pin.OUT)
# E1 = Pin(18, Pin.OUT)
# E2 = Pin(19, Pin.OUT)
# RS = Pin(10, Pin.OUT)

D4 = Pin(26, Pin.OUT)
D5 = Pin(27, Pin.OUT)
D6 = Pin(28, Pin.OUT)
D7 = Pin(29, Pin.OUT)
E1 = Pin(12, Pin.OUT)
E2 = Pin(13, Pin.OUT)
RS = Pin(5, Pin.OUT)

# Commands
LCD_CLEARDISPLAY        = 0x01
LCD_RETURNHOME          = 0x02
LCD_ENTRYMODESET        = 0x04
LCD_DISPLAYCONTROL      = 0x08
LCD_CURSORSHIFT         = 0x10
LCD_FUNCTIONSET         = 0x20
LCD_SETCGRAMADDR        = 0x40
LCD_SETDDRAMADDR        = 0x80

# Entry flags
LCD_ENTRYRIGHT          = 0x00
LCD_ENTRYLEFT           = 0x02
LCD_ENTRYSHIFTINCREMENT = 0x01
LCD_ENTRYSHIFTDECREMENT = 0x00

# Control flags
LCD_DISPLAYON           = 0x04
LCD_DISPLAYOFF          = 0x00
LCD_CURSORON            = 0x02
LCD_CURSOROFF           = 0x00
LCD_BLINKON             = 0x01
LCD_BLINKOFF            = 0x00

# Move flags
LCD_DISPLAYMOVE         = 0x08
LCD_CURSORMOVE          = 0x00
LCD_MOVERIGHT           = 0x04
LCD_MOVELEFT            = 0x00

# Function set flags
LCD_8BITMODE            = 0x10
LCD_4BITMODE            = 0x00
LCD_2LINE               = 0x08
LCD_1LINE               = 0x00
LCD_5x10DOTS            = 0x04
LCD_5x8DOTS             = 0x00



def delay_microseconds(microseconds):
    # Busy wait in loop because delays are generally very short (few microseconds).
    end = time.time() + (microseconds/1000000.0)
    while time.time() < end:
        pass


def write8(value, enable_pin, char_mode=False):
        """Write 8-bit value in character or data mode.  Value should be an int
        value from 0-255, and char_mode is True if character data or False if
        non-character data (default).
        """
        #print(f'write8', bin(value), char_mode)
        print('write8', f'{value:#010b}', enable_pin, char_mode)
        # One millisecond delay to prevent writing too quickly.
        delay_microseconds(1000)

        # Set the character/data bit
        RS.value(1 if char_mode else 0)

        # Write the Upper 4 bits
        D4.value(((value >> 4) & 1) > 0)
        D5.value(((value >> 5) & 1) > 0)
        D6.value(((value >> 6) & 1) > 0)
        D7.value(((value >> 7) & 1) > 0)

        enable_pin.off()
        delay_microseconds(1)
        enable_pin.on()
        delay_microseconds(1)
        enable_pin.off()
        delay_microseconds(1)

        # Write the Lower 4 bits
        D4.value((value        & 1) > 0)
        D5.value(((value >> 1) & 1) > 0)
        D6.value(((value >> 2) & 1) > 0)
        D7.value(((value >> 3) & 1) > 0)

        enable_pin.off()
        delay_microseconds(1)
        enable_pin.on()
        delay_microseconds(1)
        enable_pin.off()
        delay_microseconds(1)

def clear():
    print('Clear')
    write8(LCD_CLEARDISPLAY, E1)  # command to clear display
    delay_microseconds(3000)  # 3000 microsecond sleep, clearing the display takes a long time
    write8(LCD_CLEARDISPLAY, E2)


def initialize():
    print('Initializing')
    # Initialize display control, function, and mode registers.
    displaycontrol = LCD_DISPLAYON | LCD_CURSOROFF | LCD_BLINKOFF
    displayfunction = LCD_4BITMODE | LCD_1LINE | LCD_2LINE | LCD_5x8DOTS
    displaymode = LCD_ENTRYLEFT | LCD_ENTRYSHIFTDECREMENT

    for enable_pin in E1, E2:
        write8(0x33, enable_pin)
        write8(0x32, enable_pin)
        # Write registers.
        write8(LCD_DISPLAYCONTROL | displaycontrol, enable_pin)
        write8(LCD_FUNCTIONSET | displayfunction, enable_pin)
        write8(LCD_ENTRYMODESET | displaymode, enable_pin)  # set the entry mode
    clear()


if __name__ == '__main__':
    initialize()
    # Initialize the display.
    for char in 'Hello World':
        write8(ord(char), E1, True)
    for char in 'Foo Bar! +~!123':
        write8(ord(char), E2, True)
 