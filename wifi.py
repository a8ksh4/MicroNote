import time, network

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

def aps_to_dicts(aps):
    ap_keys = ('ssid', 'rssi', 'auth', 'bssid', 'channel')
    aps = [dict(zip(ap_keys, ap)) for ap in aps]
    return aps
    

def get_scanner():
    global wlan
    
    networks = set()
    while True:
        scan_result = wlan.scan()
        for ap in scan_result:
            networks.add(ap)
        yield aps_to_dicts(networks)

def join_network(ap, ssid, key):
    global wlan
    
    print(dir(wlan))
    #ssid = str(ap['ssid'])
    #ssid = "foobar"
    #channel = ap['channel']
    security = wlan.WPA_PSK
    #print(help(wlan.config))
    try:
        wlan.connect(essid=ssid,
                key=key,
                security=security)#, #'WEP', 'WPA_PSK
                #channel=channel)
        print(dir(wlan.ifconfig))
        ip = wlan.ifconfig()[0]
    except:
        ip = 'failed'
    print(f"AP mode started. SSID: {ssid} IP: {ip}")
    #.format(SSID, wlan.ifconfig()[0]))
    return ip

def get_ip():
    return wlan.ifconfig()[0]

            

#print("Scanning...")
#while (True):
#    scan_result = wlan.scan()
#    for ap in scan_result:
#        print("Channel:%d RSSI:%d Auth:%d BSSID:%s SSID:%s"%(ap))
#    print()
#    time.sleep_ms(1000)
