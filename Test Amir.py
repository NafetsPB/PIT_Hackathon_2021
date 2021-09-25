# Installed via pip: pylgbst, bleak, pygatt
import time
#from pylgbst import *
from pylgbst import get_connection_auto, get_connection_bluegiga
from pylgbst.hub import MoveHub
from pylgbst.peripherals import TiltSensor, VisionSensor, Voltage, COLORS
from random import randrange

class Callbacks:
    """Collection of callback functions"""

    @staticmethod
    def button(state):
        #Event with state = 2 gets sent directly after state = 1?
        if state == 1:
            print("Button has been pressed!")
        if state == 0:
            print("Button has been released!")

    @staticmethod
    def tilt3AxDegree(roll, pitch, yaw):
        print("Roll: %s / Pitch: %s / Yaw: %s" % (roll, pitch, yaw))

    @staticmethod
    def tilt2AxSimple(state):
        print("State: " + str(TiltSensor.DUO_STATES[state]))
    
    @staticmethod
    def visionLuminosity(luminosity):
        print("Luminosity: " + str(luminosity))
    
    @staticmethod
    def visionColorDistance(color, distance):
        print("Color: " + str(COLORS[color]))
        # Distance multiplied by 2.54 to convert inches to cm
        print("Distance: " + str(round(distance*2.54, 2)))
    
    @staticmethod
    def getDistance(distance):
        distanceInCM = round(distance*2.54, 2)
        print("Distance: " + str(distanceInCM) + "cm")
        return distanceInCM
        
class FeatureDemo:
    """Demo-Class for various features"""

    def __init__(self, hub):
        self.movehub = hub
    
    # Lists all peripheral devices
    def listPeripherals(self):
        
        for device in self.movehub.peripherals:
            print("Device: "  + str(self.movehub.peripherals[device]))

    # Lists and sets LED to all available colors
    def listLEDColors(self, delay: int = 5):

        print("Colors: " + str(COLORS))
        for color in COLORS:
            print("Setting LED color to: " + str(COLORS[color]))
            self.movehub.led.set_color(color)
            time.sleep(delay)
    
    # Spins motors A&B forwards and backwards, order: AB, A, B, external
    def spinMotor(self, time: int = 5, speed: float = 0.2):

        print("Spinning both motors forwards for " + str(time) + " seconds, with a speedValue of " + str(speed))
        self.movehub.motor_AB.timed(time, speed)
        
        print("Spinning both motors backwards for " + str(time) + " seconds, with a speedValue of -" + str(speed))
        self.movehub.motor_AB.timed(time, -speed)

        print("Spinning motor A forwards for " + str(time) + " seconds, with a speedValue of -" + str(speed))
        self.movehub.motor_A.timed(time, speed)

        print("Spinning motor A backwards for " + str(time) + " seconds, with a speedValue of -" + str(speed))
        self.movehub.motor_A.timed(time, -speed)
    
        print("Spinning motor B forwards for " + str(time) + " seconds, with a speedValue of -" + str(speed))
        self.movehub.motor_B.timed(time, speed)

        print("Spinning motor B backwards for " + str(time) + " seconds, with a speedValue of -" + str(speed))
        self.movehub.motor_B.timed(time, -speed)

        print("Spinning external motor forwards for " + str(time) + " seconds, with a speedValue of -" + str(speed))
        self.movehub.motor_external.timed(time, speed)

        print("Spinning external motor backwards for " + str(time) + " seconds, with a speedValue of -" + str(speed))
        self.movehub.motor_external.timed(time, -speed)
    
    def getVoltage(self):

        print("Value L: " + str(self.movehub.voltage.get_sensor_data(Voltage.VOLTAGE_L)))
        print("Value S: " + str(self.movehub.voltage.get_sensor_data(Voltage.VOLTAGE_S)))    
        
    def testTilt(self, duration: int = 30):

        # 3 Axis in Degrees
        self.movehub.tilt_sensor.subscribe(Callbacks.tilt3AxDegree, mode=TiltSensor.MODE_3AXIS_ACCEL)
        time.sleep(duration)
        self.movehub.tilt_sensor.unsubscribe(Callbacks.tilt3AxDegree)
        
        # 2 Axis, Simple
        self.movehub.tilt_sensor.subscribe(Callbacks.tilt2AxSimple, mode=TiltSensor.MODE_2AXIS_SIMPLE)
        time.sleep(duration)
        self.movehub.tilt_sensor.unsubscribe(Callbacks.tilt2AxSimple)

    def testButton(self, duration: int = 30):
        self.movehub.button.subscribe(Callbacks.button)
        time.sleep(duration)
        self.movehub.button.unsubscribe(Callbacks.button)
      
    def testVision(self, duration: int = 30):

        # Luminosity
        self.movehub.vision_sensor.subscribe(Callbacks.visionLuminosity, mode=VisionSensor.AMBIENT_LIGHT)
        time.sleep(duration)
        self.movehub.vision_sensor.unsubscribe(Callbacks.visionLuminosity)

        # Color and Distance
        # TODO: Split into color/distance callback
        self.movehub.vision_sensor.subscribe(Callbacks.visionColorDistance, mode=VisionSensor.COLOR_DISTANCE_FLOAT)
        time.sleep(duration)
        self.movehub.vision_sensor.unsubscribe(Callbacks.visionColorDistance)

class Vernie:
    """Class for moving Vernie"""

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

    def moveAround(self):

        def callback(distance):
            distanceInCM = round(distance*2.54, 2)
            print("Distance: " + str(distanceInCM) + "cm")
            if(distanceInCM >= 20):
                self.moveForwards(time = 1.5)
            elif(distanceInCM >= 5):
                self.moveForwards(time= 0.5)
                turnDirection = randrange(1)
                if(turnDirection == 0):
                    self.turnLeft()
                else:
                    self.turnRight()

        self.hub.vision_sensor.subscribe(callback, mode=VisionSensor.DISTANCE_INCHES)
        time.sleep(30)
        self.hub.vision_sensor.unsubscribe(callback)

    def moveForever(self):

        while True:
            self.moveForwards(time=0.3)
            self.turnRight()


# Get BT-Connection to Move Hub
conn = get_connection_bluegiga(hub_name='Move Hub')
#conn = get_connection_auto(MoveHub.DEFAULT_NAME)

try:
    hub = MoveHub(conn)
    vernie = Vernie(hub, turnAngle=500)
    #vernie.moveForever()

# Disconnect from hub, to avoid problems when connecting again later
finally:
    hub.disconnect()