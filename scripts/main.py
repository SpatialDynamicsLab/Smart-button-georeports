import sys
import time
import network
import wifiCfg
from m5stack import *
from m5ui import *
from uiflow import *
from flow import ezdata
import urequests
import unit

sys.path.append("/flash/apps")
from wifi_utils import *
from gps_simple import *

setScreenColor(0x111111)

wifi_logs = M5TextBox(130, 5, " ", lcd.FONT_Default, 0xFFFFFF, rotate=90)
btn_indicator = M5Circle(67, 180, 32, 0xcccccc, 0xcccccc)

gps_logger = M5TextBox(15, 5, "GPS:", lcd.FONT_Default, 0xFFFFFF, rotate=90)
sat_logs = M5TextBox(15, 45, "-", lcd.FONT_Default, 0xFFFFFF, rotate=90)
# print_logs = M5TextBox(15, 30, "", lcd.FONT_Default, 0xFFFFFF, rotate=90)

M5Led.on()
wait(1)
M5Led.off()


def set_app():
    setScreenColor(0x111111)
    get_wifi_status()
    # wifi_logs = M5TextBox(130, 5, " ", lcd.FONT_Default, 0xFFFFFF, rotate=90)

    # latitude = M5TextBox(90, 10, "lat-coord.", lcd.FONT_DejaVu18, 0xFFFFFF, rotate=90)
    # longitude = M5TextBox(65, 10, "long-coord.", lcd.FONT_DejaVu18, 0xFFFFFF, rotate=90)
    gps_logger = M5TextBox(15, 5, "GPS:", lcd.FONT_Default, 0xFFFFFF, rotate=90)
    sat_logs = M5TextBox(15, 45, " ", lcd.FONT_Default, 0xFFFFFF, rotate=90)

    btn_indicator = M5Circle(67, 180, 32, 0xcccccc, 0xcccccc)


def buttonA_wasPressed():
    setScreenColor(0x111111)
    gps_logger = M5TextBox(15, 5, "GPS:", lcd.FONT_Default, 0xFFFFFF, rotate=90)
    btn_indicator.setBgColor(0xffff99)
    try:
        ezdata.setData('C6J5te2z8Qfr5rkLPXCeRUkyjW3kSAgB', 'latitude',
                       gps_0.latitude)
        req = urequests.request(
            method='GET',
            url='https://v2.jokeapi.dev/joke/Programming',
            headers={}
        )
        resp = req.json()
        btn_indicator.setBgColor(0x33ff33)
        # latitude.setText("Data")
        # longitude.setText("saved")
        sat_logs.setText("GPS location saved")
    except Exception as ex:
        btn_indicator.setBgColor(0xff0000)
        sat_logs.setText("GPS location not saved")

    wait(3)
    lcd.clear()
    set_app()


def buttonB_wasPressed():
    get_wifi()
    pass


btnA.wasPressed(buttonA_wasPressed)
btnB.wasPressed(buttonB_wasPressed)

set_app()
load_gps()