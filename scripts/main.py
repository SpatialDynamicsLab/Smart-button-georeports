import sys
from m5stack import *
from m5ui import *
from uiflow import *
from flow import ezdata
# import urequests

sys.path.append("/flash/apps")
from wifi_utils import *
from gps_simple import *

setScreenColor(0x111111)

title0 = M5Title(title="Georeporting Btn.", x=3, fgcolor=0xFFFFFF, bgcolor=0x0000FF)
wifi_logs = M5TextBox(130, 30, "Wifi -", lcd.FONT_Default, 0xFFFFFF, rotate=90)
btn_indicator = M5Circle(67, 180, 32, 0xcccccc, 0xcccccc)
gps_logger = M5TextBox(15, 30, "GPS:", lcd.FONT_Default, 0xFFFFFF, rotate=90)
sat_logs = M5TextBox(15, 72, "-", lcd.FONT_Default, 0xFFFFFF, rotate=90)
btn_indicator = M5Circle(67, 180, 32, 0xcccccc, 0xcccccc)
geo_status = M5TextBox(130, 95, "", lcd.FONT_Default, 0x33ff33, rotate=90)

M5Led.on()
wait(1)
M5Led.off()


def set_app():
    setScreenColor(0x111111)
    get_wifi_status()
    title0 = M5Title(title="Georeporting Btn.", x=3, fgcolor=0xFFFFFF, bgcolor=0x0000FF)
    wifi_logs = M5TextBox(130, 30, "", lcd.FONT_Default, 0xFFFFFF, rotate=90)
    gps_logger = M5TextBox(15, 30, "GPS:", lcd.FONT_Default, 0xFFFFFF, rotate=90)
    btn_indicator = M5Circle(67, 180, 32, 0xcccccc, 0xcccccc)
    geo_status = M5TextBox(130, 95, "", lcd.FONT_Default, 0x33ff33, rotate=90)


def btn_a_was_pressed():
    get_wifi_status()
    gps_logger = M5TextBox(15, 30, "GPS:", lcd.FONT_Default, 0xFFFFFF, rotate=90)
    sat_logs.setText("")
    btn_indicator.setBgColor(0xffff99)
    try:
        # sending data for testing here:
        # https://ezdata.m5stack.com/share/?type=table&sid=mgIWDt2YyyUoj72Qj87X08oYRhUrraPb
        ezdata.setData('C6J5te2z8Qfr5rkLPXCeRUkyjW3kSAgB', 'geolocation',
                       str(gps_0.latitude, gps_0.latitude))
        btn_indicator.setBgColor(0x33ff33)
        geo_status.setText("GPS location saved")
    except Exception as ex:
        btn_indicator.setBgColor(0xff0000)
        geo_status.setText("GPS loc. not saved")

    wait(5)
    set_app()


def btn_b_was_pressed():
    get_wifi()
    pass


btnA.wasPressed(btn_a_was_pressed)
btnB.wasPressed(btn_b_was_pressed)

set_app()
load_gps()
