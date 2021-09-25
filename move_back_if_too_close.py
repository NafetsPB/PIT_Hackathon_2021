from pylgbst.hub import MoveHub, VisionSensor
from pylgbst import get_connection_bluegiga

too_close = False

def callback_sensor(distance):
    global too_close
    if distance < 3:
        too_close = True
    else:
        too_close = False

def loop():
    global too_close        
    if too_close:
        hub.motor_AB.timed(0.5, -1)

conn = get_connection_bluegiga(hub_mac="00:16:53:BA:44:01")

try:
    hub = MoveHub(conn)
    print("Connected to the Lego Boost Move Hub!")

    hub.vision_sensor.subscribe(callback_sensor, mode=VisionSensor.DISTANCE_INCHES)

    while True:
        loop()

finally:
    conn.disconnect()
