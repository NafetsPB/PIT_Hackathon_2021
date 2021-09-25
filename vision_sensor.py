from pylgbst import get_connection_bluegiga
from pylgbst.hub import MoveHub
from pylgbst.peripherals import VisionSensor, COLORS,LEDRGB,COLOR_BLACK,COLOR_RED
import time
import keyboard


ichHabeMichBewegt=False


def callback_rgb(r, g, b):
    global hub
    global ichHabeMichBewegt
    #print("Color: R = %s G = %s B = %s" % (r, g, b))
    if ichHabeMichBewegt==False:
        #print("Suche farbe")
        if r in range(70,80) and g in range(50,60) and b in range(55,65):
            ichHabeMichBewegt=True 
            hub.motor_external.angled(25,0.2)
            hub.motor_AB.timed(1.5,0.2)#Vorwärts(Rot) 
            hub.motor_external.angled(-25,0.2) 
        elif r in range(80,100) and g in range(80,100) and b in range(150,160):
            ichHabeMichBewegt=True 
            hub.motor_AB.angled(240,-0.1,0.1)#links(Gelb) 
        elif r in range(10,20) and g in range (40,50) and b in range(85,95):
            ichHabeMichBewegt=True
            hub.motor_AB.angled(240,0.1,-0.1)#rechts(Blau)   
        elif r in range(20,35) and g in range(60,80)  and b in range(120,130):
            ichHabeMichBewegt=True
            hub.motor_external.angled(-25,0.2)
            hub.motor_AB.timed(1.5,-0.2)#Rückwärts(Grün) 
            hub.motor_external.angled(25,0.2) 
        elif r in range(90,110) and g in range(90, 110) and b in range(110,130):
            print("white")
    else:
        #print("Lege mich schlafen")
        time.sleep(0.5)
        #print("Habe geschlafen.")
        ichHabeMichBewegt=False


    
def callback_color(color, distance):
    print("Color: %s distance: %s",COLORS[color],distance)  
    print("Farb_Wert: %f",color)  

conn = get_connection_bluegiga(hub_mac="00:16:53:BA:44:01")  # ! don't put this into `try` block
try:
    hub = MoveHub(conn)
    hub.led.set_color(COLOR_RED)
    hub.vision_sensor.subscribe(callback_rgb, mode=VisionSensor.COLOR_RGB)
    keyboard.wait('esc') # play with sensor while it waits   
    hub.vision_sensor.unsubscribe(callback_rgb)
finally:
    conn.disconnect()
