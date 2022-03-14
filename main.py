import smbus
# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Simple demo of the TCS34725 color sensor.
# Will detect the color from the sensor and print it out every second.
import time
import board
import adafruit_tcs34725
from adafruit_servokit import ServoKit
import knn

# Create sensor object, communicating over the board's default I2C bus
i2c = board.I2C()  # uses board.SCL and board.SDA
sensor = adafruit_tcs34725.TCS34725(i2c)
print(sensor.active)
print(sensor.integration_time)
kit = ServoKit(channels=16)

kit.servo[0].angle = 0
time.sleep(2)
kit.servo[0].angle = 60
# Change sensor integration time to values between 2.4 and 614.4 milliseconds
# sensor.integration_time = 150

# Change sensor gain to 1, 4, 16, or 60
# sensor.gain = 4


# Data is a dictionary of 5(?)-tuple: motor-angle
training_data = {}
running = False

# Add a data point (temp and lux not necessary but doable)



def go_to_angle(theta):
    # Write code to make the motor go to theta (0-360)


def button_pressed_callback(channel):
    if (training_button):
        training_data[sensor.color_rgb_bytes] = "Servo angle"
        running = False
    if (run_button):
        running = True
    print("Button pressed!")

# Main loop. Two modes Running and not. Not running is when we are training
# Running is when it should just react to what it "sees"
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
