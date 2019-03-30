# Importing the socket library to use for the transmission and receiving of UDP strings
import socket
import serial
import time
from evdev import InputDevice, categorize, ecodes

# The address used to receive UDP strings
# The port that will be used to receive UDP strings
ser = serial.Serial('/dev/ttyS0',9600,timeout = 1)
safe_forward = 44
safe_reverse = 84

l_stop = 64
r_stop = 191
left = l_stop
change = 0 
right = r_stop
ALL_STOP = 0
fail_safe = "STOP"

gamepad = InputDevice('/dev/input/event0')
aBtn = 304
bBtn = 305
xBtn = 307
yBtn = 308
R1 = 311
L1 = 310
R2 = 313
L2 = 312

#def udp_read():
#	DirectionDictionary = {"LEFT": "ThingL", "FORWARD": "ThingF", "BACK": "ThingB", "RIGHT": "ThingR","STOP": "ThingS"}
#	data, address = UDPSocket.recvfrom(1024)
#	packet = data.decode().upper()
#	if packet in DirectionDictionary:
#		print(packet)
#		return packet
# Defining the dictionary that will house the key/value pairs for the controls
#DirectionDictionary = {"LEFT": LEFT, "FORWARD": FORWARD, "BACK": BACK, "RIGHT": RIGHT,"STOP": STOP}
# Creating a socket object, using AF_INET(IPV4) and SOCK_DGRAM (socket type constant)
#UDPSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Binding the socket object to a pre-defined address and port
#UDPSocket.bind((UDP_IP_Address, UDP_Port_Number))

#function to adjust velocity
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
def LEFT(left, right):
	#reduce speed of Motor 1
	left = inertia(left, l_stop)
	ser.write( bytes([left]) )
	print("M1 = ", left)
	return 1

#function to turn right
def RIGHT(left, right):
	#reduce speed of Motor 2
	right = inertia(right, r_stop)
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
	#ser.write( bytes([left]))
	#ser.write( bytes([right]))
	ser.write( bytes ([ALL_STOP]))
	print("M1 = ", left)
	print("M2 = ", right)
	print("ALL STOP")
	return 1
#function that calls on functions
def switch_func(Data):
	#search for Packet Value in DirectionDictionary
	DirectionDictionary = {"LEFT": LEFT, "FORWARD": FORWARD, "BACK": BACK, "RIGHT": RIGHT,"STOP": STOP}
	func = DirectionDictionary.get(Data)
	return func(left, right)

#Data = udp_read()
# While true loop to continuously listen for UDP transmissions
while True:
	# recvfrom receives a pair of values, string & address, where string is the string representing the data being sent
	# & address is the address of the socket sending the data
	# All of the above is preceded by a number of bytes to receive from a transmission
	# Example = socket.recvfrom(BufferSize[,flags])
	#data, address = UDPSocket.recvfrom(1024)
	# As long as the transmission isn't empty
	# Create a string from the transmission of type byte and capitalize its letters
	#Data = udp_read()

	#function that calls on functions
	#def switch_func(Data):
	#	#search for Packet Value in DirectionDictionary
	#	DirectionDictionary = {"LEFT": LEFT, "FORWARD": FORWARD, "BACK": BACK, "RIGHT": RIGHT,"STOP": STOP}
	#	func = DirectionDictionary.get(Data)
	#	return func(left, right)

	#print("Packet: ",Data)
	#change = switch_func(Data)
	#if change == 1:
		#fail_safe = Data
		#print("Change = ", change)
		#Data = udp_read()
	#else:
		#Data = fail_safe
		#change = switch_func(Data)
		
	for event in gamepad.read_loop():
    #filters by event type
		if event.type == ecodes.EV_KEY:
					if event.value == 1:
						if event.code == aBtn:
							print("A Pressed")
							FORWARD()
						elif event.code == bBtn:
							print("B Pressed")
							STOP()
						elif event.code == xBtn:
							print("X Pressed")
						elif event.code == yBtn:
							print("Y Pressed")
							BACK()
						elif event.code == R1:
							print("R1 Pressed")
						elif event.code == R2:
							print("R2 Pressed")
						elif event.code == L1:
							print("L1 Pressed")
						elif event.code == L2:
							print("L2 Pressed")
						
					if event.value == 0:
						if event.code == aBtn:
							print("A Released")
						elif event.code == bBtn:
							print("B Released")
							STOP()
						elif event.code == xBtn:
							print("X Released")
						elif event.code == yBtn:
							print("Y Released")
						elif event.code == R1:
							print("R1 Pressed")
						elif event.code == R2:
							print("R2 Pressed")
						elif event.code == L1:
							print("L1 Pressed")
						elif event.code == L2:
							print("L2 Pressed")
