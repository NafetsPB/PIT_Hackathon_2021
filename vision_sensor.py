from pylgbst import get_connection_bluegiga
from pylgbst.hub import MoveHub
from pylgbst.peripherals import VisionSensor, COLORS
import time

def callback(r, g, b):
    print("Color: R = %s G = %s B = %s" % (r, g, b))
    if r >= 18 and g >= 15 and b >= 12:
        print("RED")
    elif r in range(15,20) and g in range(18,30) and b in range(25,40):
        print("YELLOW")
    elif r >= 2 and g >= 12 and b >= 19:
        print("BLUE")
    elif r >= 6 and g >= 18 and b >= 26:
        print("GREEN")
    elif r >= 19 and g >= 23 and b >= 35:
        print("ORANGE")
    elif r >= 23 and g >= 26 and b >= 24:
        print("WHITE")
    

conn = get_connection_bluegiga(hub_mac="00:16:53:BA:44:01")  # ! don't put this into `try` block
try:
    hub = MoveHub(conn)

    hub.vision_sensor.subscribe(callback, mode=VisionSensor.COLOR_RGB)
    time.sleep(240) # play with sensor while it waits   
    hub.vision_sensor.unsubscribe(callback)
finally:
    conn.disconnect()
