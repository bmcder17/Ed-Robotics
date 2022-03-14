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
READ_STATE = False

running = True

def training_pressed_callback(channel):
    train_data[sensor.color_rgb_bytes] = read_angle()
    running = False
    print("training pressed!")

def testing_pressed_callback(channel):
    running = True
    print("Button pressed!")


# GPIO init.
GPIO.setmode(GPIO.BCM)
GPIO.setup(ASK_GPIO, GPIO.OUT)
GPIO.output(ASK_GPIO, READ_STATE)
GPIO.setup(TRAIN_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(TRAIN_BUTTON, GPIO.RISING, 
        callback=training_pressed_callback, bouncetime=100)
GPIO.setup(TEST_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(TEST_BUTTON, GPIO.RISING, 
        callback=testing_pressed_callback, bouncetime=100)

# Serial Init
ser = serial.Serial ("/dev/ttyS0", 9600)    #Open port with baud rate
GPIO.cleanup()
ser.reset_input_buffer()

# Data is a dictionary of 5(?)-tuple: motor-angle
training_data = {}
#running = False

# Add a data point (temp and lux not necessary but doable)



def go_to_angle(theta):
    # Write code to make the motor go to theta (0-135)
    if theta > 135:
        theta = 135
    elif theta < 0:
        theta = 0
    theta_p = theta / 135
    pulse = (1750*theta_p) + 500
    
def read_angle():
    READ_STATE = not(READ_STATE)
    GPIO.output(ASK_GPIO, READ_STATE)
    received_data = ser.read() #read serial port
    sleep(0.03)
    data_left = ser.inWaiting()
    received_data += ser.read(data_left)
    print(received_data)
    servo_angle = int(received_data)
    #print(servo_angle)
    return servo_angle


# Main loop. Two modes Running and not. Not running is when we are training
# Running is when it should just react to what it "sees"
try:
    while True:
        print(running)
        if running:
           print('what')
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