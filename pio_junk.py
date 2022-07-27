from machine import Pin
import rp2
from rp2 import PIO

@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
def blink():
    wrap_target()
    set(pins, 1)   [31]
    nop()          [31]
    nop()          [31]
    nop()          [31]
    nop()          [31]
    set(pins, 0)   [31]
    nop()          [31] 
    nop()          [31]
    nop()          [31]
    nop()          [31]
    wrap()

# sm = rp2.StateMachine(0, pio_junk.blink, freq=2000, set_base=Pin(6))
# sm.active(1)


@rp2.asm_pio(sideset_init=rp2.PIO.OUT_LOW)
def side_blink():
    wrap_target()
    # set(pins, 1)   [31]
    set(x, 31).side(0x0)
    label("aloop")
    nop()           [7]
    jmp(x_dec, "aloop")

    # set(pins, 0)   [31]
    set(x, 31).side(0x1)
    label("bloop")
    nop()           [7]
    jmp(x_dec, "bloop")
    wrap()

# sm = rp2.StateMachine(0, pio_junk.side_blink, freq=2000, sideset_base=Pin(6))
# sm.active(1)


@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
def blink_1hz():
    # Cycles: 1 + 1 + 6 + 32 * (30 + 1) = 1000
    irq(rel(0))
    set(pins, 1)
    set(x, 31)                  [5]
    label("delay_high")
    nop()                       [29]
    jmp(x_dec, "delay_high")

    # Cycles: 1 + 7 + 32 * (30 + 1) = 1000
    set(pins, 0)
    set(x, 31)                  [6]
    label("delay_low")
    nop()                       [29]
    jmp(x_dec, "delay_low")


@rp2.asm_pio(set_init=(PIO.IN_HIGH, PIO.IN_HIGH, PIO.IN_HIGH, PIO.IN_HIGH, 
                        PIO.IN_HIGH, PIO.IN_HIGH, PIO.IN_HIGH, PIO.IN_HIGH, ))
def query_pins_1hz():
    set(x, null)
    wrap_target()
    label("read_loop")
    irq(rel(1))           [31]
    mov(y, pins)          [31]  # read the button pins
    jmp(x == y, "read_loop")  # start over if no keys changed
    set(x, y)                   # copy y regester to x register
    mov(isr, y)                 # move y regerter values to isr
    push()                      # push the isr value to the fifo
    irq(rel(0))                 # signal that bottons have chaged
    wrap()                      # start over


@rp2.asm_pio( sideset_init=PIO.OUT_LOW,
              set_init=[PIO.IN_HIGH for n in range(16)] )
def echo_pins_side():
    wrap_target()
    mov(isr, null)
    mov(isr, pins)  .side(0x0)  
    # in(pins)        .side(0x0)
    push()

    set(x, 31)                 
    label("aloop")
    nop()                       [7]
    jmp(x_dec, "aloop")

    mov(isr, null)  .side(0x1) 
    push()

    set(x, 31)               
    label("bloop")
    nop()                       [7]
    jmp(x_dec, "bloop")

    wrap()


@rp2.asm_pio( set_init=[PIO.IN_HIGH]*32 )
def echo_pins():
    wrap_target()
    in_(pins, 32)
    push()

    set(x, 31)                 
    label("aloop")
    nop()                       [31]
    jmp(x_dec, "aloop")

    wrap()


@rp2.asm_pio( set_init=[PIO.IN_HIGH]*32 )
def echo_pins_changes():
    mov(y, pins)
    #in_(y, 32)
    mov(isr, y)
    push()

    wrap_target()
    label("read loop")
    mov(x, pins)

    jmp(x_not_y, "exit read loop")
    jmp("read loop")
    label("exit read loop")
    
    mov(isr, x)
    mov(y, x)
    push()

    wrap()


@rp2.asm_pio( set_init=[PIO.IN_HIGH]*32 )
def irq_pins_changes():
    mov(y, pins)
    #in_(y, 32)
    mov(isr, y)
    push()

    wrap_target()
    label("read loop")
    mov(x, pins)

    jmp(x_not_y, "exit read loop")
    jmp("read loop")
    label("exit read loop")
    
    mov(isr, x)
    mov(y, x)
    push()
    irq(1)

    wrap()
