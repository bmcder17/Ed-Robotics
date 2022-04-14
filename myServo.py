from servoExample import PCA9685
import time
import smbus

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
pwm.setServoPulse(0, 1000)  #  500 output 102 0x0066 0.5ms ~170mV
time.sleep(2)
pwm.setServoPulse(0, 2000)  # 2250 output 460 0x01CC 2.25ms ~710mV
time.sleep(2)
pwm.setServoPulse(0, 0)  
#pwm.setServoPulse(1, 2500)

# pwm.setServoPulse(0, 2688) # output 550
# time.sleep(2)


# while True:
# 	pwm.setServoPulse(0, 1800)
# 	time.sleep(sleepTime)
# 	pwm.setServoPulse(0, 500)
# 	time.sleep(sleepTime)