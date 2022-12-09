from m5stack import *
from m5ui import *
from uiflow import *

setScreenColor(0x111111)
wifi_logs = M5TextBox(128, 25, '', lcd.FONT_Default, 0xFFFFFF, rotate=90)


def get_wifi():
    import wifiCfg
    for count in range(3):
        wait_ms(250)
        M5Led.on()
        wait_ms(250)
        M5Led.off()
    wifi_logs.setText('')
    wifi_logs.setText("Connecting to wifi...")
    # auto connect wifi
    wifiCfg.autoConnect(lcdShow=False)
    wait(2)

    if wifiCfg.wlan_sta.isconnected():
        wifi_logs.setText("Wifi connected")
        wait(1)
        wifi_logs.setText(str(wifiCfg.wlan_sta.ifconfig()[0]))
        wait(1)
        wifi_logs.setText("Wifi ok!")
        for count in range(3):
            wait_ms(250)
            M5Led.on()
            wait_ms(250)
            M5Led.off()
        return

    if not wifiCfg.wlan_sta.isconnected():
        wifi_logs.setText("Reconnecting to wifi...")
        wifiCfg.reconnect()
        is_connected()


def is_connected():
    import wifiCfg

    if wifiCfg.wlan_sta.isconnected():
        wifi_logs.setText("Wifi connected")
        wait(1)
        wifi_logs.setText(str(wifiCfg.wlan_sta.ifconfig()[0]))
        wait(1)
        wifi_logs.setText("Wifi ok!")
        for count in range(3):
            wait_ms(250)
            M5Led.on()
            wait_ms(250)
            M5Led.off()
        return
    else:
        for count in range(4):
            wifi_logs.setText("Wifi is not connected...")
            wait_ms(250)
            M5Led.on()
            wait_ms(250)
            M5Led.off()
            wifi_logs.setText("Press side button to try again")
        wifi_logs.setText("wifi n/a")


def get_wifi_status():
    import wifiCfg
    if wifiCfg.wlan_sta.isconnected():
        wifi_logs.setText("")
        wifi_logs.setText("Wifi ok!")
    else:
        wifi_logs.setText("")
        wifi_logs.setText("No wifi")
        wait(2)
        wifi_logs.setText("Press side button to connect")
        wait(4)
        wifi_logs.setText("No wifi")

        

def wifi_connect():
    import time
    import network

    wifi_logs = M5TextBox(128, 25, "-", lcd.FONT_Default, 0xFFFFFF, rotate=90)
    wifi_logs.setText("Connecting to wifi...")

    ssid = "DIGIFIBRA-ZDsk"
    password = "AYuKFD2CsH"

    station = network.WLAN(network.STA_IF)

    if station.isconnected() == True:
        print_logs.setText("Wifi already connected")
        wait(1)
        M5Led.on()
        print_logs.setText(str(station.ifconfig()[0]))
        wait(1)
        M5Led.off()
        print_logs.setText("Net.: " + str(ssid))
        return
    station.active(True)
    station.connect(ssid, password)

    while station.isconnected() == False:
        pass

    wifi_logs.setText("Wifi connection is Ok!")
    wifi_logs.setText(str(station.ifconfig()[0]))
    wifi_logs.setText("Net.: " + str(ssid))

    for count in range(3):
        wait_ms(250)
        M5Led.on()
        wait_ms(250)
        M5Led.off()

   
def hello():
    wifi_logs.setText("Hi")
    pass
