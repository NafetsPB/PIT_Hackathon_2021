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
    def visionColorDistance(distance):
        global vernie
        global goOn
        distanceInCm = round(distance*2.54, 2) 
        # Distance multiplied by 2.54 to convert inches to cm
        print("Distance: " + str(distanceInCm))
        if distanceInCm <= 15 and distanceInCm > 0:
            goOn = False
            
        else:
            goOn = True

        """time.sleep(1)
        vernie.moveForwards(time=1)
        if distanceInCm <= 15:
            print("stop")
            vernie.moveBackwards(time=0.5)
            vernie.turnLeft()

        else:
            vernie.moveForwards(time=0.5)"""


            
class FeatureDemo:
    """Demo-Class for various features"""

    def __init__(self, hub):
        self.movehub = hub

    def testVision(self, duration: int = 60):
        
        # Color and Distance
        # TODO: Split into color/distance callback
        self.movehub.vision_sensor.subscribe(Callbacks.visionColorDistance, mode=VisionSensor.DISTANCE_INCHES, granularity = 2)
        #time.sleep(duration)
        #self.movehub.vision_sensor.unsubscribe(Callbacks.visionColorDistance)



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
    


    """@staticmethod
    def visionDistance(distance):
        # Distance multiplied by 2.54 to convert inches to cm
        print("Distance: " + str(round(distance*2.54, 2))
        if distance <= 5:
            Vernie.moveBackwards()
        else:
            Vernie.moveForwards()"""

# Get BT-Connection to Move Hub
conn = get_connection_bluegiga(hub_name='Move Hub')
#conn = get_connection_auto(MoveHub.DEFAULT_NAME)

try:
    hub = MoveHub(conn)
    vernie = Vernie(hub, turnAngle=500)
    """vernie.moveForwards()
    vernie.turnLeft()
    vernie.moveBackwards()
    vernie.turnRight()
    vernie.moveForwards()"""
    demo = FeatureDemo(hub)
    demo.testVision(duration=300)
    goOn = True
    while goOn:
        vernie.moveForwards()

    while goOn == False:
        vernie.turnLeft()
        goOn = True
        #time.sleep(1)
    #Callbacks.testVision()
    #vernie.callback()
    #vernie.moveForever()

# Disconnect from hub, to avoid problems when connecting again later
finally:
    hub.disconnect()