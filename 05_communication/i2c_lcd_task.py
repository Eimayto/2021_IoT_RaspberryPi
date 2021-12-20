from lcd import drivers
from time import sleep
from datetime import datetime
import Adafruit_DHT

sensor = Adafruit_DHT.DHT11
DHT_PIN = 4

display = drivers.Lcd()

try:
    while True:
        now = datetime.now()
        display.lcd_display_string(now.strftime("%x%X"), 1)
        
        h, t = Adafruit_DHT.read_retry(sensor, DHT_PIN)
        if h is not None and t is not None:
            display.lcd_display_string('%.1f*C, %.1f%%' % (t, h),2)
        else:
            display.lcd_display_string('Read Error', 2)

finally:
    display.lcd_clear()