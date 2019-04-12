import evdev
import subprocess
import time
from evdev import InputDevice, categorize, ecodes

#checks to see if the controller is connected and will connect if needed
while True:
    try:
		#creates object 'gamepad' to store the data
        gamepad = InputDevice('/dev/input/event0')
        break
    except:
        subprocess.call(['./connect.sh'])
        time.sleep(5)
#prints out device info at start
print(gamepad)

#evdev read loop
for event in gamepad.read_loop():
    #filters by event type
	if event.type == ecodes.EV_ABS:
		print(event)
		print(int((event.value / 1.422)))
