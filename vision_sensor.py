from pylgbst import get_connection_bluegiga
from pylgbst.hub import MoveHub, VisionSensor
import time

def callback(clr, distance):
    print("Color: %s / Distance: %s" % (clr, distance))

conn = get_connection_bluegiga(hub_mac="00:16:53:BA:44:01")  # ! don't put this into `try` block
try:
    hub = MoveHub(conn)

    hub.vision_sensor.subscribe(callback, mode=VisionSensor.COLOR_DISTANCE_FLOAT)
    time.sleep(60) # play with sensor while it waits   
    hub.vision_sensor.unsubscribe(callback)
finally:
    conn.disconnect()
