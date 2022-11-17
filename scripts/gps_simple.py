from m5stack import *
from m5ui import *
from uiflow import *
import time
import unit

setScreenColor(0x111111)
# GPS UNIT INIT
gps_0 = unit.get(unit.GPS, unit.PORTA)

def load_gps():
  # UI labels
  latitude = M5TextBox(88, 35, "lat-coord.", lcd.FONT_Default, 0xFFFFFF, rotate=90)
  longitude = M5TextBox(63, 35, "long-coord.", lcd.FONT_Default, 0xFFFFFF, rotate=90)
  gps_logger = M5TextBox(15, 30, "GPS: ", lcd.FONT_Default, 0xFFFFFF, rotate=90)
  sat_logs = M5TextBox(15, 72, "Connecting...", lcd.FONT_Default, 0xFFFFFF, rotate=90)

  # GPS data
  while True:
    wait(5)
    latitude.setText(str(gps_0.latitude))
    longitude.setText(str(gps_0.longitude))
    sat_logs.setText("satellites " + str(gps_0.satellite_num))
    wait(3)
    latitude.setText(str('Getting'))
    longitude.setText(str('position...'))
    wait(2)
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

