import serial
import subprocess
import time
import RPi.GPIO as GPIO
from evdev import InputDevice, categorize, ecodes


panServo = 18
tiltServo = 17

ser = serial.Serial('/dev/ttyS0',9600,timeout = 1)
# Max forward speed
safe_forward = 30
# Max reverse speed
safe_reverse = 98
directionTurn = 0
# Left and right stop values
l_stop = 64
r_stop = 191
# these variables are used to store the speeds before turning
leftOld = 64
rightOld = 191
#change = 0 
right = r_stop
left = l_stop
ALL_STOP = 0
fail_safe = "STOP"
direction = ""

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)
#assert angle >= 30 and angle <= 165
pwmX = GPIO.PWM(18, 50)
pwmY = GPIO.PWM(17, 50)
pwmX.start(7.5)
pwmY.start(7.5)

TRIGGER_PIN = 26
ECHO_PIN = 16

GPIO.setup(TRIGGER_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)
GPIO.output(TRIGGER_PIN, False)

# checks to see if controller is connected and if it isn't connected it will attempt to connect
while True:
	try:
		gamepad = InputDevice('/dev/input/event0')
		break
	except:
		print("Gamepad not found attempting to connect now")
		# Change this to match your bluetooth connection script name
		subprocess.call(['./ControllerConnect.sh'])
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
RSX = 2
RSY = 5

def rangefind():
	TRIGGER_PIN = 26
	ECHO_PIN = 16
	time.sleep(0.1)

	print("Starting Measurement.....")

	GPIO.output(TRIGGER_PIN, True)
	time.sleep(0.00001)
	GPIO.output(TRIGGER_PIN, False)

	while GPIO.input(ECHO_PIN) == 0:
		pass
	start = time.clock()

	while GPIO.input(ECHO_PIN) == 1:
		pass
	stop = time.clock()

	print((stop - start) * 17000)
	print(start)
	print(stop)


def setServoAngle(servo, angle, axis):

	print("Angle: ", angle)
	print("Servo: ", servo)
	if angle >= 45:
		dutyCycle = angle / 15. #+ 3.
	else:
		dutyCycle = 2.5
	if axis == "x":
		pwmX.ChangeDutyCycle(dutyCycle)
	else:
		pwmY.ChangeDutyCycle(dutyCycle)
	#pwm.start(dutyCycle)
	print(dutyCycle)
	#pwm.stop()


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

	#function to turn left
def LEFT(direction):
	global left
	global right
	print(direction)
	'''Logic to check direction of travel f = forward b = reverse 
	if it is empty it will turn on the spot'''
	if direction == "f":
		left = 20
		right = right + 20
		ser.write( bytes([left]) )
		ser.write( bytes([right]) )
	elif direction == "b":
		left = 108
		right = right - 20
		ser.write( bytes([left]) )
		ser.write( bytes([right]) )
	else:
		left = 20
		right = 226
		ser.write( bytes([left]) )
		ser.write( bytes([right]) )
	print("M1 = ", left)
	print("M2 = ", right)
	return 1

	
# Takes in the old values of left and right to return to normal after turn	
def TURNSTOP(leftOld, rightOld):
	global right
	global left
	right = rightOld
	left = leftOld
	ser.write( bytes([right]) )
	ser.write( bytes([left]) )
	
#function to turn right
def RIGHT(direction):
	# Bringing in the global variables
	global right
	global left
	print(direction)
	'''Logic to check direction of travel f = forward b = reverse 
	if it is empty it will turn on the spot'''
	if direction == "f":
		right = 148
		left = left + 20
		ser.write( bytes([right]))
		ser.write( bytes([left]))
	elif direction == "b":
		right = 235
		left = 87
		ser.write( bytes([right]))
		ser.write( bytes([left]))
	else:
		right = 148
		left = 84
		ser.write( bytes([right]))
		ser.write( bytes([left]))
		
		
	return 1

#function for stopping
def STOP():
	''' Once called it will reset all values back to stop and it will
		tell the motor controller to stop any current movement'''
	global left
	global right
	left = l_stop
	right = r_stop
	leftOld = l_stop
	rightOld = r_stop
	ser.write( bytes ([ALL_STOP]))
	print("M1 = ", left)
	print("M2 = ", right)
	print("ALL STOP")
	return 1
	


while True:

		
	for event in gamepad.read_loop():
		''' this logic will check to see what key is being pressed on the gamepad 
			and will execute any code related to that button'''
		if event.type == ecodes.EV_KEY:
					print(LSXVAL)
					# when event value is 1 it is being pressed
					if event.value == 1:
						if event.code == aBtn:
							print("A Pressed")
						# B button is used as an emergency stop
						elif event.code == bBtn:
							print("B Pressed")
							STOP()
							direction = ""
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
					# when event value is 2 the button is held down									
					if event.value == 2:
						if event.code == R2:
							if LSXVAL == 128:
								FORWARD()
								direction = "f"
						if event.code == L2:
							if LSXVAL == 128:
								BACK()
								direction = "b"
					# when event value is 0 it is released			
					if event.value == 0:
						if event.code == aBtn:
							print("A Released")
							rangefind()
						elif event.code == bBtn:
							print("B Released")
						elif event.code == xBtn:
							print("X Released")
						elif event.code == yBtn:
							print("Y Released")
						elif event.code == R1:
							print("R1 Released")
						# when R2 and L2 are released it will stop the motors
						elif event.code == R2:
							STOP()
							direction = ""
							leftOld = l_stop
							rightOld = r_stop
						elif event.code == L1:
							print("L1 Released")
						elif event.code == L2:
							STOP()
							direction = ""
							leftOld = l_stop
							rightOld = r_stop
							
		if event.type == ecodes.EV_ABS:
					# Turning Right
					'''directionTurn is used to tell what way it is currently turning
						wen it is 2 it is turning right and when it is 1 it is turning left'''
					if event.code == LSX:
						LSXVAL = event.value
						if event.value == 0:
							leftOld = left
							rightOld = right
							RIGHT(direction)
							directionTurn = 2
						if event.value == 128:
							if directionTurn == 2:
								TURNSTOP(leftOld, rightOld)
								directionTurn = 0
						#Turning Left	
						if event.value == 255:
							rightOld = right
							leftOld = left
							LEFT(direction)
							directionTurn = 1
						if event.value == 128:
							if directionTurn == 1:
								TURNSTOP(leftOld, rightOld)
								#rightOld = r_stop
								#leftOld = l_stop
								directionTurn = 0
								
					# Taking input from gamepad to control the servos			
					if event.code == RSX:
						axis = "x"
						num = int(event.value / 1.422)
						print("event.value = " + str(event.value / 1.422))
						setServoAngle(panServo, num, axis)
						#GPIO.cleanup()

					if event.code == RSY:
						axis = "y"
						num = int(event.value / 1.422)
						#if num < 30 or num > 165:
							#print("")
						#else:
						setServoAngle(tiltServo, num, axis)
						#GPIO.cleanup()	

