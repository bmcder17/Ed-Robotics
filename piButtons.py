
import signal
import sys
import RPi.GPIO as GPIO
import time
BUTTON_GPIO = 12

# Known good gpios 21, 20, 26, 19, 13, 6, 5 

def signal_handler(sig, frame):
    GPIO.cleanup()
    sys.exit(0)

    
def button_pressed_callback(channel):
    print("Button pressed!")

def please():
    print("working")

if __name__ == '__main__':
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(BUTTON_GPIO, GPIO.FALLING, callback=button_pressed_callback, bouncetime=200)
    print("hi")
    #signal.signal(signal.SIGINT, signal_handler)
    print("hello")
    #signal.pause()
    message = input("fun")
    time.sleep(1)
    print("what")
    GPIO.cleanup()