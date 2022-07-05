import wifi
import oled_text as oled
import time
#import repl
import keeb
import gc

WIFI_NET = 'dkcommonwealth'
WIFI_PASS = 'Blahblah_8'

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
    while True:
        pressed = keeb.get_next()
        print("Main received key:", pressed)
        print('gc_start', time.ticks_ms())
        gc.collect()
        print('gc end', time.ticks_ms())
        if pressed == "_bspc":
            if char_buffer:
                char_buffer.pop()
        elif pressed == "_entr":
            exec_string = ''.join(char_buffer)
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


    # print('Running')
    # scanner = wifi.get_scanner()
    # networks = next(scanner)
    # for n, network in enumerate(networks):
    #     print(n, network)
    # print("which to join?")
    # n = int(input())
    # print("joining", n, networks[n])
    # print("passphrase?")
    # #k = input()
    # k = "Blahblah_8"
    # print("entered:", k)
    
    # wifi.join_network(networks[n], k)
