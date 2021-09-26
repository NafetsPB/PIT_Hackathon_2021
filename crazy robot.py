import time
#from pylgbst import *
from pylgbst import get_connection_auto, get_connection_bluegiga
from pylgbst.hub import MoveHub
from pylgbst.peripherals import COLOR_BLACK, COLOR_BLUE, COLOR_RED, TiltSensor, VisionSensor, Voltage, COLORS
from random import randrange
import keyboard 
import random



###Angegebene Parametern ,die aus Vernie wir sammeln können.
class Callbacks:

    ##Orientierung im Raum , bzw. Achse , Grad usw. 
    @staticmethod
    def tilt3AxDegree(roll, pitch, yaw):
        print("Roll: %s / Pitch: %s / Yaw: %s" % (roll, pitch, yaw))

    @staticmethod
    def tilt2AxSimple(state):
        print("State: " + str(TiltSensor.DUO_STATES[state]))

###Brightness
    @staticmethod
    def visionLuminosity(luminosity):
        print("Luminosity: " + str(luminosity))

###Ablesen aus Sensor ,die Farbe und Distanz
    @staticmethod
    def visionColorDistance(color, distance):
        print("Color: " + str(COLORS[color]))
# Distance multiplied by 2.54 to convert inches to cm, weil es war im Inches
        print("Distance: " + str(round(distance*2.54, 2)))
### Nur Distanz
    @staticmethod
    def getDistance(distance):
        global distanceInCM
        distanceInCM = round(distance*2.54, 2)
        print("Distance: " + str(distanceInCM) + "cm")
        return distanceInCM


class FeatureDemo:
    ## Initialisation of Movehub
    def __init__(self, hub):
        self.movehub = hub
    ##Sensoren
    def listPeripherals(self):
        for device in self.movehub.peripherals:
            print("Device: "  + str(self.movehub.peripherals[device]))
    ###Mechnik der Motors und Regeln für Bewegung
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
# Spannung an Batareen
    def getVoltage(self):

        print("Value L: " + str(self.movehub.voltage.get_sensor_data(Voltage.VOLTAGE_L)))
        print("Value S: " + str(self.movehub.voltage.get_sensor_data(Voltage.VOLTAGE_S)))

##Positionerung
    def testTilt(self, duration: int = 30):

        # 3 Axis in Degrees
        self.movehub.tilt_sensor.subscribe(Callbacks.tilt3AxDegree, mode=TiltSensor.MODE_3AXIS_ACCEL)
        time.sleep(duration)
        self.movehub.tilt_sensor.unsubscribe(Callbacks.tilt3AxDegree)
        
        # 2 Axis, Simple
        self.movehub.tilt_sensor.subscribe(Callbacks.tilt2AxSimple, mode=TiltSensor.MODE_2AXIS_SIMPLE)
        time.sleep(duration)
        self.movehub.tilt_sensor.unsubscribe(Callbacks.tilt2AxSimple)

#Test für Button
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

#Parametern für MoveHub
    def __init__(self, hub: MoveHub, turnAngle: int = 500, movementSpeed: float = 0.2):

        # Motor-Angle for 90-Degree turn, might need adjustment based on floortype
        self.hub = hub
        self.turnAngle = turnAngle
        self.movementSpeed = movementSpeed
    
    #Benennung der Funktionen.
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


conn = get_connection_bluegiga(hub_mac='00:16:53:B9:E7:35')

try:
    hub = MoveHub(conn)
    vernie = Vernie(hub, turnAngle=500)
    print("Begin of operation")
    begin = True
    while begin:
        a = random.random()
        if 0.6 > a >= 0.4:
            vernie.turnLeft()
        if a >= 0.8:
                vernie.moveForwards(1)
        if 0.8> a >=0.6 :
                vernie.turnRight()
        if a <= 0.3:
            vernie.moveBackwards(1)
        if keyboard.is_pressed("Esc"):
            begin = False
        time.sleep(0.5)
    


finally:
    hub.disconnect()