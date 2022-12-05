from m5stack import *
from m5ui import *
from uiflow import *
import time
import unit


setScreenColor(0x111111)
# GPS UNIT INIT
gps_0 = unit.get(unit.GPS, unit.PORTA)


def dd_formating(dd_lat, dd_long):
  lat_coord = dd_lat
  long_coord = dd_long
  try:
    if dd_lat:
      lat_coord = 'LAT'
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
    lat_coord = 'formating err.'
    long_coord = 'formating err.'
    pass

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