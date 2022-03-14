import serial
import RPi.GPIO as GPIO
import smbus
from time import sleep
ASK_GPIO = 18
LOW = GPIO.LOW
HIGH = GPIO.HIGH

ser = serial.Serial ("/dev/ttyS0", 9600)    #Open port with baud rate





def main():
	GPIO.cleanup()
	ser.reset_input_buffer()
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(ASK_GPIO, GPIO.OUT)
	GPIO.output(ASK_GPIO, LOW)
	state = 0
	ser.write(5)
	try:
		while True:
			if (state == 0):
				print('in high')
				GPIO.output(ASK_GPIO,HIGH)
				state = 1
			elif (state == 1):
				print('in low')
				GPIO.output(ASK_GPIO,LOW)
				state = 0
				print('unrad')
				test = ser.inWaiting()
				
				
				received_data = ser.read() #read serial port
				sleep(0.03)
				data_left = ser.inWaiting()
				received_data += ser.read(data_left)
				print(received_data)
				#print('here')
				
				#print('data_left')
				#
				
			#print('loop')
			sleep(1)  
	except KeyboardInterrupt:
		GPIO.cleanup()
		ser.close()

if __name__ == '__main__':
	main()
