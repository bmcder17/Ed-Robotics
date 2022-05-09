import time
import board
import serial
import RPi.GPIO as GPIO
import adafruit_tcs34725
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import knn
from servoExample import PCA9685
import smbus


# Sensor Initializations

# Servo Driver
pwm = PCA9685(0x40, debug=False)
pwm.setPWMFreq(50)
sleepTime = 2

# Color Sensor
# Create sensor object, communicating over the board's default I2C bus
i2c = board.I2C()  # uses board.SCL and board.SDA
sensor = adafruit_tcs34725.TCS34725(i2c)
print(sensor.active)
print(sensor.integration_time)

# Change sensor integration time to values between 2.4 and 614.4 milliseconds
# sensor.integration_time = 150

# Change sensor gain to 1, 4, 16, or 60
# sensor.gain = 4


# ADC Module
# Create the ADC object using the I2C bus
ads = ADS.ADS1015(i2c)
# you can specify an I2C adress instead of the default 0x48
# ads = ADS.ADS1115(i2c, address=0x49)

# Create single-ended input on channel 0
chan = AnalogIn(ads, ADS.P0)

# GPIO Definitions
TEST_BUTTON = 21
RESET_BUTTON = 20
TRAIN_BUTTON = 1
TEST_LED = 26
RESET_LED = 19
TRAIN_LED = 6
SENS_LED = 5
#READ_STATE = False

running = True

# Interrupt handler function definitions

# All of the interrupt functions control their respective LEDs. The LEDs are 
# timed to help indicate when Teddy is "thinking" or "busy" a.k.a. modes where 
# we do not want the user actively moving Teddy's arm

# Training Button function. Here is where we add new data to the training data 
# dictionary with the 3-tuple of RGB as the key and the servo postion as the 
# corresponding value 
def training_pressed_callback(channel):
    GPIO.output(TRAIN_LED, 1)
    time.sleep(1)
    #print("training")
    training_data[current_color] = read_angle() 
    #print(training_data)
    time.sleep(1.25)
    GPIO.output(TRAIN_LED, 0)
    #print("training pressed!")

# Testing Button function. For this function, we wait a bit to give the user 
# more time to line up whatever colored object Teddy is observering. We also 
# check for a None result which indicates that no training has been done and 
# Teddy's nose will flicker to indicate that something went wrong. If there is 
# a valid goal for the servo, we wait to convey that Teddy is thinking before 
# moving to the goal as dictated by the KNN result
def testing_pressed_callback(channel):
    GPIO.output(TEST_LED, 1)
    time.sleep(1)
    goal = target_angle
    if goal == None:
        GPIO.output(RESET_LED, 1)
        time.sleep(0.2)
        GPIO.output(RESET_LED, 0)
        time.sleep(0.2)
        GPIO.output(RESET_LED, 1)
        time.sleep(0.2)
        GPIO.output(RESET_LED, 0)
        time.sleep(0.2)
        GPIO.output(RESET_LED, 1)
        time.sleep(0.2)
        GPIO.output(RESET_LED, 0)
        return
    else:
        GPIO.output(TEST_LED, 0)
        time.sleep(0.25)
        GPIO.output(TEST_LED, 1)
        time.sleep(0.75)
        #print(goal)
        go_to_angle(goal)
        GPIO.output(TEST_LED, 0)
        #print("testing pressed!")

# Reset Button funtion. This simply clears the training data and flashes the 
# red LED briefly
def reset_pressed_callback(channel):
    GPIO.output(RESET_LED, 1)
    training_data.clear()
    time.sleep(1)
    GPIO.output(RESET_LED, 0)
    #print("reset!!!!")
  


# GPIO Initializations, this includes all LEDs and Buttons
GPIO.setmode(GPIO.BCM)
GPIO.setup(TEST_LED, GPIO.OUT)
GPIO.output(TEST_LED, 0)
GPIO.setup(RESET_LED,GPIO.OUT)
GPIO.output(RESET_LED, 0)
GPIO.setup(TRAIN_LED,GPIO.OUT)
GPIO.output(TRAIN_LED, 0)
GPIO.setup(SENS_LED,GPIO.OUT)
GPIO.output(SENS_LED, 1)
GPIO.setup(TRAIN_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(TRAIN_BUTTON, GPIO.FALLING, 
        callback=training_pressed_callback, bouncetime=300)
GPIO.setup(TEST_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(TEST_BUTTON, GPIO.FALLING, 
        callback=testing_pressed_callback, bouncetime=300)
GPIO.setup(RESET_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(RESET_BUTTON, GPIO.FALLING, 
        callback=reset_pressed_callback, bouncetime=300)


# Data is a dictionary of 3-tuple: motor-angle
training_data = {}





# Function to move the pointer to the target angle, we ended up only needing 
# approximately 125 degrees but the equation works so well that we didn't want 
# to mess with it
def go_to_angle(theta):
    #print("move")
    theta_p = theta / 135
    pulse = ((2250-500)*theta_p)+500 
    pwm.setServoPulse(0,pulse)
    time.sleep(0.5)
    pwm.setServoPulse(0,0)
    
# Function to read the servo position from the ADC. Then the servo angle is 
# converted from the raw format into a degrees. We check the edge cases to make 
# sure the measured angle isn't exceeding our inteded boundaries and correct 
# them in necessary     
def read_angle():
    servo_angle = chan.value
    print("raw: {:>5}".format(servo_angle))
    servo_angle = round(((servo_angle-4480)/(18800-4480)) * 135, 2)
    print("raw: {:>5f}".format(servo_angle))
    test = False
    if servo_angle > 125:
        servo_angle_deg = 125
    elif servo_angle < 0:
        servo_angle_deg = 0
    else:
        servo_angle_deg = servo_angle
    return servo_angle_deg


# Main loop. The target_angle and current_color variable are declared as 
# global so that the interrupt handler functions can use them. The current_color is continously updating the global variable to whatever it sees and the target_angle is also updating from the KNN model.

try:
    
    global target_angle
    global current_color
    while True:
        print(training_data)
        current_color = sensor.color_rgb_bytes
        time.sleep(0.01)
        target_angle = knn.nearest_neighbor(training_data, current_color)
        #print("target")
        #print(target_angle
        time.sleep(0.5)


except KeyboardInterrupt:
    # Clean up on exit
    GPIO.cleanup()
