# Installed via pip: pylgbst, bleak, pygatt
import time
#from pylgbst import *
from pylgbst import get_connection_auto, get_connection_bluegiga
from pylgbst import hub
from pylgbst.hub import MoveHub
from pylgbst.peripherals import TiltSensor, VisionSensor, Voltage, COLORS
from random import randrange

class Callbacks:
    """Collection of callback functions"""


    @staticmethod
    def visionColor_RGB(r,g,b):
        global vernie
        print("Color: R = %s G = %s B = %s" % (r, g, b))
        if r in range(70,80) and g in range(50,60) and b in range(55,65):
            print("RED")
        elif r in range(80,100) and g in range(80,100) and b in range(150,160):
            print("YELLOW")
        elif r in range(10,20) and g in range (40,50) and b in range(85,95):
            print("BLUE")
        elif r in range(20,35) and g in range(60,80)  and b in range(120,130):
            print("GREEN")
        elif r in range(90,110) and g in range(90, 110) and b in range(110,130):
            print("WHITE")
            
class FeatureDemo:
    """Demo-Class for various features"""

    def __init__(self, hub):
        self.movehub = hub

    def testVision(self, duration: int = 60):
        
        # Color and Distance
        # TODO: Split into color/distance callback
        self.movehub.vision_sensor.subscribe(Callbacks.visionColor_RGB, mode=VisionSensor.COLOR_RGB)
        time.sleep(duration)
        self.movehub.vision_sensor.unsubscribe(Callbacks.visionColor_RGB)



class Vernie:
    """Class for moving Vernie"""
    def __init__(self, hub):
        self.movehub = hub

    def __init__(self, hub: MoveHub, turnAngle: int = 500, movementSpeed: float = 0.2):

        # Motor-Angle for 90-Degree turn, might need adjustment based on floortype
        self.hub = hub
        self.turnAngle = turnAngle
        self.movementSpeed = movementSpeed
    
    def turnRight(self):
        self.hub.motor_A.angled(self.turnAngle, self.movementSpeed)

    def turnLeft(self):
        self.hub.motor_B.angled(self.turnAngle, self.movementSpeed)

    def moveForwards(self, time: float = 1.0):
        self.hub.motor_AB.timed(time, self.movementSpeed)

    def moveBackwards(self, time: float = 1.0):
        self.hub.motor_AB.timed(time, -self.movementSpeed)

# Get BT-Connection to Move Hub
conn = get_connection_bluegiga(hub_mac="00:16:53:BA:44:01")
#conn = get_connection_auto(MoveHub.DEFAULT_NAME)

try:
    hub = MoveHub(conn)
    vernie = Vernie(hub, turnAngle=500)
    demo = FeatureDemo(hub)
    demo.testVision(duration=300)

# Disconnect from hub, to avoid problems when connecting again later
finally:
    hub.disconnect()