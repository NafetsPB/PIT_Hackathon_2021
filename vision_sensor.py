from pylgbst import get_connection_bluegiga
from pylgbst.hub import MoveHub
from pylgbst.peripherals import VisionSensor, COLORS
import time

def callback(r, g, b):
    print("Color: R = %s G = %s B = %s" % (r, g, b))

conn = get_connection_bluegiga(hub_mac="00:16:53:BA:44:01")  # ! don't put this into `try` block
try:
    hub = MoveHub(conn)

    hub.vision_sensor.subscribe(callback, mode=VisionSensor.COLOR_RGB)
    time.sleep(60) # play with sensor while it waits   
    hub.vision_sensor.unsubscribe(callback)
finally:
    conn.disconnect()
