#import smbus
# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Simple demo of the TCS34725 color sensor.
# Will detect the color from the sensor and print it out every second.
import time
import board
import serial
import adafruit_tcs34725
from adafruit_servokit import ServoKit
import knn
from servoExample import PCA9685
import smbus

# Servo Driver
pwm = PCA9685(0x40, debug=True)
pwm.setPWMFreq(50)
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

# Defines
TEST_BUTTON = 23
TRAIN_BUTTON = 24
RESET_BUTTON = 25
ASK_GPIO = 18
LOW = GPIO.LOW
HIGH = GPIO.HIGH

running = True
training = !running

# GPIO init.
GPIO.setmode(GPIO.BCM)
GPIO.setup(ASK_GPIO, GPIO.OUT)
GPIO.output(ASK_GPIO, LOW)
GPIO.setup(TRAIN_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(BUTTON_GPIO, GPIO.RISING, 
        callback=train_pressed_callback, bouncetime=100)
GPIO.setup(TRAIN_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(BUTTON_GPIO, GPIO.RISING, 
        callback=train_pressed_callback, bouncetime=100)

# Data is a dictionary of 5(?)-tuple: motor-angle
training_data = {}
running = False

# Add a data point (temp and lux not necessary but doable)

# Serial Init
ser = serial.Serial ("/dev/ttyS0", 9600)    #Open port with baud rate
GPIO.cleanup()
ser.reset_input_buffer()

def go_to_angle(theta):
    # Write code to make the motor go to theta (0-135)
    theta_p = theta / 135
    pulse = (1750*theta_p) + 500
    
def read_angle():


def training_pressed_callback(channel):
    train_data[sensor.color_rgb_bytes] = "Servo angle"
    running = False
    print("Button pressed!")

def testing_pressed_callback(channel):
    running = True
print("Button pressed!")

# Main loop. Two modes Running and not. Not running is when we are training
# Running is when it should just react to what it "sees"
try:
    while True:
        if running:
           target_angle = knn.nearest_neighbor(training_data, sensor.color_rgb_bytes)
           go_to_angle(target_angle)
        time.sleep(0.1)









        # Raw data from the sensor in a 4-tuple of red, green, blue, clear light component values
        # print(sensor.color_raw)

        color = sensor.color
        color_rgb = sensor.color_rgb_bytes
        print(
            "RGB color as 8 bits per channel int: #{0:02X} or as 3-tuple: {1}".format(
                color, color_rgb
            )
        )

        # Read the color temperature and lux of the sensor too.
        temp = sensor.color_temperature
        lux = sensor.lux
        print("Temperature: {0}K Lux: {1}\n".format(temp, lux))
        # Delay for a second and repeat.
        time.sleep(1.0)
except KeyboardInterrupt:
    GPIO.cleanup()
    ser.close()