from pylgbst import get_connection_bluegiga
from pylgbst.hub import MoveHub
from pylgbst.peripherals import VisionSensor, COLORS,LEDRGB,COLOR_BLACK,COLOR_RED
import time

def callback_rgb(r, g, b):
    global hub
    #print("Color: R = %s G = %s B = %s" % (r, g, b))
    if r in range(70,80) and g in range(50,60) and b in range(55,65):
        hub.motor_AB.timed(0.9,-0.5)#Rückwärts(Rot)    
    elif r in range(80,100) and g in range(80,100) and b in range(150,160):
        hub.motor_AB.timed(0.5,-0.5,0.5)#links(Gelb)
    elif r in range(10,20) and g in range (40,50) and b in range(85,95):
        hub.motor_AB.timed(0.5,0.5,-0.5)#rechts(Blau)  
    elif r in range(20,35) and g in range(60,80)  and b in range(120,130):
        hub.motor_AB.timed(0.9,0.5)#Vorwärts(Grün)  
    elif r in range(90,110) and g in range(90, 110) and b in range(110,130):
        print("white")


    
def callback_color(color, distance):
    print("Color: %s distance: %s",COLORS[color],distance)  
    print("Farb_Wert: %f",color)  

conn = get_connection_bluegiga(hub_mac="00:16:53:BA:44:01")  # ! don't put this into `try` block
try:
    hub = MoveHub(conn)
    hub.led.set_color(COLOR_RED)
    hub.vision_sensor.subscribe(callback_rgb, mode=VisionSensor.COLOR_RGB)
    time.sleep(240) # play with sensor while it waits   
    hub.vision_sensor.unsubscribe(callback_rgb)
finally:
    conn.disconnect()
