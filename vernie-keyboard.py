from pylgbst import get_connection_bluegiga
from pylgbst.hub import MoveHub
import keyboard

def move_a(self):
    global hub
    hub.motor_AB.start_speed(1, 1)

def stop_a(self):
    global hub
    hub.motor_AB.stop()

keyboard.on_press_key('a', move_a)
keyboard.on_release_key('a', stop_a)

conn = get_connection_bluegiga(hub_mac="00:16:53:B9:E7:35")  # ! don't put this into `try` block

try:
    hub = MoveHub(conn)
    keyboard.wait('esc')
finally:
    conn.disconnect()
