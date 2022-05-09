from servoExample import PCA9685
import time
import smbus
import board
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn


# Create the I2C bus
i2c = board.I2C()
# Create the ADC object using the I2C bus
ads = ADS.ADS1015(i2c)
# you can specify an I2C adress instead of the default 0x48
# ads = ADS.ADS1115(i2c, address=0x49)

# Create single-ended input on channel 0
chan = AnalogIn(ads, ADS.P0)

# Create differential input between channel 0 and 1
# chan = AnalogIn(ads, ADS.P0, ADS.P1)

print("{:>5}\t{:>5}".format("raw", "v"))

    

pwm = PCA9685(0x40, debug=True)
pwm.setPWMFreq(50)
sleepTime = 2



# MG996R Servo values
#pwm.setServoPulse(0,588) # out 120
#time.sleep(2)
#pwm.setServoPulse(0,1395) # ~90 deg
#time.sleep(2)
#pwm.setServoPulse(0, 2200) # out 450

# SG90 Servo values
# start input 549 output 112
# end input 2688 output 550 
pwm.setServoPulse(0, 500)  # pulse:500 value:4480 voltage:0.56V 
time.sleep(2)
print("{:>5}\t{:>5.3f}".format(chan.value, chan.voltage))
time.sleep(0.5)
print("{:>5}\t{:>5.3f}".format(chan.value, chan.voltage))
time.sleep(2)
pwm.setServoPulse(0, 2120)  # pulse:2250  value:18784  voltage:2.35V 
time.sleep(2)
print("{:>5}\t{:>5.3f}".format(chan.value, chan.voltage))
time.sleep(2)
input()
pwm.setServoPulse(0, 0)  
#pwm.setServoPulse(1, 2500)

# pwm.setServoPulse(0, 2688) # output 550
# time.sleep(2)


# while True:
# 	pwm.setServoPulse(0, 1800)
# 	time.sleep(sleepTime)
# 	pwm.setServoPulse(0, 500)
# 	time.sleep(sleepTime)