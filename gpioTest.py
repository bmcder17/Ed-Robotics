
import signal
import sys
import RPi.GPIO as GPIO
import time
BUTTON_GPIO = 21

def signal_handler(sig, frame):
    GPIO.cleanup()
    sys.exit(0)

    
def button_pressed_callback(channel):
    print("Button pressed!")

def please():
    print("working")

if __name__ == '__main__':
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTON_GPIO, GPIO.OUT)
    GPIO.output(BUTTON_GPIO, 1)
    time.sleep(2)
    #GPIO.add_event_detect(BUTTON_GPIO, GPIO.RISING, callback=please, bouncetime=200)
    print("hi")
    #signal.signal(signal.SIGINT, signal_handler)
    print("hello")
    #signal.pause()
    message = input("yes")
    GPIO.output(BUTTON_GPIO, 0)
    GPIO.cleanup()