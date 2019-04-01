import serial
import subprocess
import time
from evdev import InputDevice, categorize, ecodes


ser = serial.Serial('/dev/ttyS0',9600,timeout = 1)
safe_forward = 30
safe_reverse = 98
directionTurn = 0
l_stop = 64
r_stop = 191
left = l_stop
leftOld = 64
rightOld = 191
change = 0 
right = r_stop
ALL_STOP = 0
fail_safe = "STOP"
direction = ""

# checks to see if controller is connected and if it isn't connected it will attempt to connect
while True:
	try:
		gamepad = InputDevice('/dev/input/event0')
		break
	except:
		print("Gamepad not found attempting to connect now")
		subprocess.call(['./connect.sh'])
		time.sleep(5)
# Button values for controller
aBtn = 304
bBtn = 305
xBtn = 307
yBtn = 308
R1 = 311
L1 = 310
R2 = 313
L2 = 312
LSX = 00
LSXVAL = 128

def inertia(Mvalue, Mrestrict): #Mrestrict is the integer that you do not want the result to exceed
	rate = 0.25 #the rate at which we will adjust the speed. 
	start_value = Mvalue - Mrestrict;
	result = start_value * (1 - rate) 
	command = result + Mrestrict
	print("Mvalue = " ,Mvalue)
	print("Command = " ,command)
	return int(command)

def BACK():
	global left
	global right
	left = inertia(left, safe_reverse)
	right = inertia(right, (safe_reverse + 127))
	ser.write( bytes([left]) )
	ser.write( bytes([right]))
	print("M1 = ", left)
	print("M2 = " , right)
	return 1

	#function for moving forward
def FORWARD():
	global left
	global right
	left = inertia(left, safe_forward)
	right = inertia(right, (safe_forward + 127))
	ser.write( bytes([left]) )
	ser.write( bytes([right]))
	print("M1 = ", left)
	print("M2 = ", right)
	return 1

	#fucntion to turn left
def LEFT(direction):
	global left
	global right
	if direction == "f":
		left = 20
		ser.write( bytes([left]) )
	else:
		left = 108
		ser.write( bytes([left]) )
	print("M1 = ", left)
	print("M2 = ", right)
	return 1
# Once the turn is complete this will return the wheels speed value back to normal
def LEFTS(leftOld):
	global left
	left = leftOld
	ser.write( bytes([left]) )
	
def RIGHTS(rightOld):
	global right
	print("Right Old: " ,rightOld)
	right = rightOld
	ser.write( bytes([right]) )
	
#function to turn right
def RIGHT(direction):
	#reduce speed of Motor 2
	global right
	if direction == "f":
		right = 147
		ser.write( bytes([right]))
	else:
		right = 235
		ser.write( bytes([right]))
	print("M2 = ", right)
	return 1

#function for stopping
def STOP():
	#loop for safely reducing speed
	global left
	global right
	left = l_stop
	right = r_stop
	leftOld = l_stop
	rightOld = r_stop
	#ser.write( bytes([left]))
	#ser.write( bytes([right]))
	ser.write( bytes ([ALL_STOP]))
	print("M1 = ", left)
	print("M2 = ", right)
	print("ALL STOP")
	return 1

while True:

		
	for event in gamepad.read_loop():

		if event.type == ecodes.EV_KEY:
					print(LSXVAL)							
					if event.value == 1:
						if event.code == aBtn:
							print("A Pressed")
						elif event.code == bBtn:
							print("B Pressed")
							STOP()
						elif event.code == xBtn:
							print("X Pressed")
						elif event.code == yBtn:
							print("Y Pressed")
						elif event.code == R1:
							print("R1 Pressed")
						elif event.code == R2:
							FORWARD()
							print("R2 Pressed")
						elif event.code == L1:
							print("L1 Pressed")
						elif event.code == L2:
							BACK()
														
					if event.value == 2:
						if event.code == R2:
							if LSXVAL == 128:
								FORWARD()
								direction = "f"
						if event.code == L2:
							if LSXVAL == 128:
								BACK()
								direction = "b"
					if event.value == 0:
						if event.code == aBtn:
							print("A Released")
							STOP()
							direction = ""
						elif event.code == bBtn:
							print("B Released")
							STOP()
							direction = "f"
						elif event.code == xBtn:
							print("X Released")
						elif event.code == yBtn:
							print("Y Released")
						elif event.code == R1:
							print("R1 Pressed")
						elif event.code == R2:
							STOP()
							direction = "f"
						elif event.code == L1:
							print("L1 Pressed")
						elif event.code == L2:
							STOP()
							direction = "f"
							
		if event.type == ecodes.EV_ABS:
					if event.code == LSX:
						LSXVAL = event.value
						if event.value == 0:
							leftOld = left
							LEFT(direction)
							directionTurn = 2
						if event.value == 128:
							if directionTurn == 2:
								LEFTS(leftOld)
								leftOld = l_stop
								directionTurn = 0
							
						if event.value == 255:
							rightOld = right
							RIGHT(direction)
							directionTurn = 1
						if event.value == 128:
							if directionTurn == 1:
								RIGHTS(rightOld)
								rightOld = r_stop
								directionTurn = 0

							
