import sys
from m5stack import *
from m5ui import *
from uiflow import *
from flow import ezdata
import urequests
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
  latitude = M5TextBox(88, 35, "lat-coord.", lcd.FONT_Default, 0xFFFFFF, rotate=90)
  longitude = M5TextBox(63, 35, "long-coord.", lcd.FONT_Default, 0xFFFFFF, rotate=90)
  gps_logger = M5TextBox(15, 30, "GPS: ", lcd.FONT_Default, 0xFFFFFF, rotate=90)
  sat_logs = M5TextBox(15, 72, "Connecting...", lcd.FONT_Default, 0xFFFFFF, rotate=90)

  # GPS data
  while True:
    coords = dd_formating(gps_0.latitude, gps_0.longitude)
    wait(3)
    try:
      latitude.setText(str(coords[0]))
      longitude.setText(str(coords[1]))
    except Exception:
      latitude.setText(str(gps_0.latitude))
      longitude.setText(str(gps_0.longitude))
    sat_logs.setText("satellites " + str(gps_0.satellite_num))
    wait(5)
    latitude.setText(str('Getting'))
    longitude.setText(str('position...'))
    if str(gps_0.satellite_num) == "00":
      latitude.setText("-")
      longitude.setText("-")
      sat_logs.setText("")
      sat_logs.setText(str(gps_0.pos_quality))
    else:
      for count in range(3):
        wait_ms(250)
        M5Led.on()
        wait_ms(250)
        M5Led.off()
        sat_logs.setText("")
        sat_logs.setText("Ok!")


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
        ezdata.setData('C6J5te2z8Qfr5rkLPXCeRUkyjW3kSAgB', 'geolocation', str(dd_formating(gps_0.latitude, gps_0.longitude)))
        req = urequests.request(method='POST', url='https://api-ucd-community-georeports.kaizenmaps.com/api/v2/spatialdynamicslab/datasets/cycling-safety/places', json={
          "type": "Feature",
          "geometry": {
              "type": "Point",
              "coordinates": [
                  longitude.setText(str(coords[1])),
                  latitude.setText(str(coords[0]))
              ]
          },
          "properties": {
              "visible": "on",
              "location_type": "cyclist-hazard",  
              "submitter_name": str(api_key)
          }
      }, headers={'Authorization': 'Api-Key kx4l16yF.q1gHBjnPuQziHE9KCVRpTRMkyWfdo1Gz'})
                       
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
