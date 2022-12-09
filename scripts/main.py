import sys
from m5stack import *
from m5ui import *
from uiflow import *
from flow import ezdata
import urequests
import json
import time
import unit
import deviceCfg

sys.path.append("/flash/apps")
from wifi_utils import *

setScreenColor(0x111111)
# GPS UNIT INIT
gps_0 = unit.get(unit.GPS, unit.PORTA)
# macaddr = wifiCfg.wlan_sta.config('mac')
# macaddr = '{:02x}:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}'.format(*macaddr)
api_key=deviceCfg.get_apikey()


def sending_data():
    triangle0 = M5Triangle(67, 198, 44, 222, 90, 222, 0xFFFFFF, 0xFFFFFF)
    wait_ms(300)
    triangle1 = M5Triangle(67, 159, 44, 184, 90, 184, 0xFFFFFF, 0xFFFFFF)
    wait_ms(300)
    triangle2 = M5Triangle(67, 120, 44, 145, 90, 145, 0xFFFFFF, 0xFFFFFF)
    wait_ms(300)
    wait(1)
    triangle0.hide()
    triangle1.hide()
    triangle2.hide()


def sending_data_true():
    triangle0 = M5Triangle(67, 198, 44, 222, 90, 222, 0xFFFFFF, 0xFFFFFF)
    wait_ms(500)
    triangle1 = M5Triangle(67, 159, 44, 184, 90, 184, 0xFFFFFF, 0xFFFFFF)
    wait_ms(500)
    triangle2 = M5Triangle(67, 120, 44, 145, 90, 145, 0xFFFFFF, 0xFFFFFF)
    wait_ms(500)
    circle0 = M5Circle(67, 70, 30, 0x33cc00, 0x33cc00)

M5Led.on()
wait_ms(500)
M5Led.off()
welcome1 = M5TextBox(95, 40, "Welcome to your", lcd.FONT_DejaVu18, 0xFFFFFF, rotate=90)
welcome2 = M5TextBox(63, 22, "georeporting button", lcd.FONT_DejaVu18, 0xFFFFFF, rotate=90)
wait(3)
welcome1.hide()
welcome2.hide()
sending_data()
wait(1)
setScreenColor(0x111111)


def set_app():
    setScreenColor(0x111111)
    title0 = M5Title(title="Georeporting Btn.", x=3, fgcolor=0xFFFFFF, bgcolor=0x0000FF)
    wifi_logs = M5TextBox(128, 25, "", lcd.FONT_Default, 0xFFFFFF, rotate=90)
    gps_logger = M5TextBox(15, 25, "GPS:", lcd.FONT_Default, 0xFFFFFF, rotate=90)
    sat_logs = M5TextBox(15, 65, "", lcd.FONT_Default, 0xFFFFFF, rotate=90)
    geo_status = M5TextBox(130, 95, "", lcd.FONT_Default, 0x33ff33, rotate=90)
    get_wifi_status()


def btn_a_was_pressed():
    get_wifi_status()
    data = {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [
              dd_formating(gps_0.latitude, gps_0.longitude)[1],
              dd_formating(gps_0.latitude, gps_0.longitude)[0]
            ]
        },
        "properties": {
            "visible": "on",
            "location_type": "cyclist-hazard",
            "submitter_name": str(api_key)
        }
    }
    api_headers = {'Authorization': 'Api-Key kx4l16yF.q1gHBjnPuQziHE9KCVRpTRMkyWfdo1Gz'}
    gps_logger = M5TextBox(15, 25, "GPS:", lcd.FONT_Default, 0xFFFFFF, rotate=90)
    geo_status = M5TextBox(130, 95, "", lcd.FONT_Default, 0x33ff33, rotate=90)
    try:
      sending_data()
      response = urequests.request(
        method='POST',
        url='https://api-ucd-community-georeports.kaizenmaps.com/api/v2/spatialdynamicslab/datasets/cycling-safety/places',
        json=data, 
        headers=api_headers
      )
      sending_data()
      sending_data_true()
      geo_status.setText("GPS location saved")
    except Exception as ex:
      ezdata.setData('C6J5te2z8Qfr5rkLPXCeRUkyjW3kSAgB', 'info', str(ex))
      geo_status.setColor(0xff0000)
      geo_status.setText("GPS loc. not saved")
    
    wait(2)
    setScreenColor(0x111111)
    set_app()


def buttonA_wasDoublePress():
    get_wifi_status()
    data = {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [
              dd_formating(gps_0.latitude, gps_0.longitude)[1],
              dd_formating(gps_0.latitude, gps_0.longitude)[0]
            ]
        },
        "properties": {
            "visible": "on",
            "location_type": "citizen-near-miss-report",
            "submitter_name": str(api_key)
        }
    }
    api_headers = {'Authorization': 'Api-Key kx4l16yF.q1gHBjnPuQziHE9KCVRpTRMkyWfdo1Gz'}
    gps_logger = M5TextBox(15, 25, "GPS:", lcd.FONT_Default, 0xFFFFFF, rotate=90)
    geo_status = M5TextBox(130, 95, "", lcd.FONT_Default, 0x33ff33, rotate=90)
    try:
      sending_data()
      response = urequests.request(
        method='POST',
        url='https://api-ucd-community-georeports.kaizenmaps.com/api/v2/spatialdynamicslab/datasets/cycling-safety/places',
        json=data, 
        headers=api_headers
      )
      sending_data()
      sending_data_true()
      geo_status.setText("GPS location saved")
    except Exception as ex:
      ezdata.setData('C6J5te2z8Qfr5rkLPXCeRUkyjW3kSAgB', 'info', str(ex))
      geo_status.setColor(0xff0000)
      geo_status.setText("GPS loc. not saved")
    
    wait(2)
    setScreenColor(0x111111)
    set_app()



def btn_b_was_pressed():
    get_wifi()
    pass


def dd_formating(dd_lat, dd_long):
  lat_coord = dd_lat
  long_coord = dd_long
  try:
    if dd_lat:
      north_dir = dd_lat.find('N')
      if north_dir != -1:
        get_lat = float(dd_lat.split('N')[0]) / 100
      else:
        get_lat = -float(dd_lat.split('S')[0]) / 100
      lat_coord = get_lat
    if dd_long:
      east_dir = dd_long.find('E')
      if east_dir != -1:
        get_long = float(dd_long.split('E')[0]) / 100
      else:
        get_long = -float(dd_long.split('W')[0]) / 100
      long_coord = get_long
  except Exception as ex:
    pass
    return False

  return lat_coord, long_coord
  

def load_gps():
  # UI labels
  latitude = M5TextBox(88, 35, "", lcd.FONT_Default, 0xFFFFFF, rotate=90)
  longitude = M5TextBox(63, 35, "", lcd.FONT_Default, 0xFFFFFF, rotate=90)
  gps_logger = M5TextBox(15, 25, "GPS: ", lcd.FONT_Default, 0xFFFFFF, rotate=90)
  sat_logs = M5TextBox(15, 65, "Connecting...", lcd.FONT_Default, 0xFFFFFF, rotate=90)
  # GPS data
  while True:
    latitude.setText('')
    longitude.setText('')
    triangle0 = M5Triangle(67, 198, 44, 222, 90, 222, 0xFFFFFF, 0xFFFFFF)
    sat_logs.setText("Ok! satellites no. " + str(gps_0.satellite_num))
    circle0 = M5Circle(67, 70, 20, 0xFFFFFF, 0xFFFFFF)
    wait_ms(500)
    circle0.setSize(25)
    wait_ms(250)
    if gps_0.satellite_num and str(gps_0.satellite_num) != "00":
      sat_logs.setText("Ok! satellites no. " + str(gps_0.satellite_num))
      circle0.setSize(30)
      wait_ms(500)
      circle0.setSize(20)
      wait_ms(500)
      circle0.setSize(25)
    else:
      wait_ms(250)
      M5Led.on()
      wait_ms(250)
      M5Led.off()
      latitude.setColor(0xff0000)
      longitude.setColor(0xff0000)
      latitude.setText('While GPS is inactive it is')
      longitude.setText('impossible to send reports')
      sat_logs.setText("")
      sat_logs.setText("Waiting for signal")
      wait(1)
      sat_logs.setText(str(gps_0.pos_quality))
      
btnA.wasPressed(btn_a_was_pressed)
btnA.wasDoublePress(buttonA_wasDoublePress)
btnB.wasPressed(btn_b_was_pressed)

set_app()
load_gps()
