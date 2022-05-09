#import smbus
# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Simple demo of the TCS34725 color sensor.
# Will detect the color from the sensor and print it out every second.
import time
import board
import serial
import RPi.GPIO as GPIO
import adafruit_tcs34725
from adafruit_servokit import ServoKit
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import knn
from servoExample import PCA9685
import smbus

# Known good gpios 21, 20, 26, 19, 13, 6, 5 


# Servo Driver
#pwm = PCA9685(0x40, debug=True)
#pwm.setPWMFreq(50)
sleepTime = 2

# Create sensor object, communicating over the board's default I2C bus
i2c = board.I2C()  # uses board.SCL and board.SDA
sensor = adafruit_tcs34725.TCS34725(i2c)
print(sensor.active)
print(sensor.integration_time)

# Change sensor integration time to values between 2.4 and 614.4 milliseconds
# sensor.integration_time = 150

# Change sensor gain to 1, 4, 16, or 60
# sensor.gain = 4

# Create the ADC object using the I2C bus
ads = ADS.ADS1115(i2c)
# you can specify an I2C adress instead of the default 0x48
# ads = ADS.ADS1115(i2c, address=0x49)

# Create single-ended input on channel 0
chan = AnalogIn(ads, ADS.P0)

# Defines
TEST_BUTTON = 21
RESET_BUTTON = 20
TRAIN_BUTTON = 1
LED1_GPIO = 26
LED2_GPIO = 19
LED3_GPIO = 6
#READ_STATE = False

running = True

# Interrupt handler function definitions

def training_pressed_callback(channel):
    training_data[sensor.color_rgb_bytes] = read_angle()
    #running = True
    print("training pressed!")

def testing_pressed_callback(channel):
    #running = True
    #global target_angle
    #go_to_angle(target_angle)
    print("testing pressed!")

def reset_pressed_callback(channel):
    print("reset!!!!")
    pass


# GPIO init.
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED1_GPIO, GPIO.OUT)
GPIO.output(LED1_GPIO, 0)
GPIO.setup(LED2_GPIO,GPIO.OUT)
GPIO.output(LED2_GPIO, 0)
GPIO.setup(LED3_GPIO,GPIO.OUT)
GPIO.output(LED3_GPIO, 0)
GPIO.setup(TRAIN_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(TRAIN_BUTTON, GPIO.FALLING, 
        callback=training_pressed_callback, bouncetime=200)
GPIO.setup(TEST_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(TEST_BUTTON, GPIO.FALLING, 
        callback=testing_pressed_callback, bouncetime=200)
GPIO.setup(RESET_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(RESET_BUTTON, GPIO.FALLING, 
        callback=reset_pressed_callback, bouncetime=200)


# Data is a dictionary of 5(?)-tuple: motor-angle
training_data = {}
running = False

# Add a data point (temp and lux not necessary but doable)



def go_to_angle(theta):
    print("move")
    # Write code to make the motor go to theta (0-135)
    
    theta_p = theta / 135
    pulse = (260*theta_p)-250 
    pwm.setServoPulse(pulse)
    sleep(0.5)
    pwm.setServoPulse(0)
    
def read_angle():
    #READ_STATE = not(READ_STATE)
    servo_angle = chan.value
    print("raw: {:>5}".format(servo_angle))
    servo_angle = round(((servo_angle-4480)/(18800-4480)) * 135, 2)
    print("raw: {:>5f}".format(servo_angle))
    if servo_angle > 135:
        servo_angle = 123.75
    elif servo_angle < 112.5:
        servo_angle = 101.24
    elif servo_angle =
    return servo_angle


# Main loop. Two modes Running and not. Not running is when we are training
# Running is when it should just react to what it "sees"
try:
    while True:
        global target_angle
        read_angle()
        #print(running)
        if running:
            
           #print('what')
           #GPIO.output(LED_GPIO,1)
            time.sleep(0.01)
            target_angle = knn.nearest_neighbor(training_data, sensor.color_rgb_bytes)
           #GPIO.output(LED_GPIO,0)
           #go_to_angle(target_angle)
        time.sleep(0.1)









        # Raw data from the sensor in a 4-tuple of red, green, blue, clear light component values
        # print(sensor.color_raw)

        color = sensor.color
        color_rgb = sensor.color_rgb_bytes
        #print(
        #    "RGB color as 8 bits per channel int: #{0:02X} or as 3-tuple: {1}".format(
        #        color, color_rgb
         
        #   )
        #)
        #print(type(color_rgb[1]))
        # Read the color temperature and lux of the sensor too.
        temp = sensor.color_temperature
        lux = sensor.lux
        #print("Temperature: {0}K Lux: {1}\n".format(temp, lux))
        # Delay for a second and repeat.
        time.sleep(1.0)


except KeyboardInterrupt:
    # Clean up on exit
    GPIO.cleanup()
