from spike import PrimeHub, LightMatrix, Button, StatusLight, ForceSensor, MotionSensor, Speaker, ColorSensor, App, DistanceSensor, Motor, MotorPair
from spike.control import wait_for_seconds, wait_until, Timer
from math import *
import json


hub = PrimeHub()
ports = ['A', 'B', 'C', 'D', 'E', 'F']

# Not idempotent. Removes port from ports when it finds a thing
def find_thing(thing):
    ret = None
    remove = None
    for port in ports:
        try:
            ret = thing(port)
            remove = port
            break
        except:
            pass
    ports.remove(remove)
    return ret

motor = find_thing(Motor)
color = find_thing(ColorSensor)
motor2 = find_thing(Motor)

def euclidean_distance_sq(loc, other):
    tot = 0
    for i in range(len(loc)):
        tot += (loc[i] - other[i]) ** 2
    return tot

def clear_buttons():
    hub.left_button.was_pressed()
    hub.right_button.was_pressed()

def setup_get_sensor_data(color_sensor):
    #return lambda : (color_sensor.get_rgb_intensity()[0]*1024/(color_sensor.get_rgb_intensity()[3]+1),color_sensor.get_rgb_intensity()[1]*1024/(color_sensor.get_rgb_intensity()[3]+1))
    return lambda : (color_sensor.get_rgb_intensity()[0],color_sensor.get_rgb_intensity()[1])


def train_menu():
    train = False
    hub.light_matrix.show_image('GO_RIGHT')
    clear_buttons()
    while True:
        if hub.motion_sensor.was_gesture('tapped'):
            return train
        if hub.left_button.was_pressed() or hub.right_button.was_pressed():
            train = not train
            if train:
                hub.light_matrix.write('T')
            else:
                hub.light_matrix.show_image('GO_RIGHT')

def choose(loc, data):
    return min(map(lambda kv : (euclidean_distance_sq(loc, kv[0]), kv[1]), data.items()))[1]

def send(thing):
    print(json.dumps(thing))

def train(get_sensor_data, motor, motor2 = None):
    data = {}
    choices = ['CHESSBOARD', 'GO_RIGHT']
    choice = 0
    hub.light_matrix.show_image(choices[choice])
    while True:
        if hub.left_button.was_pressed():
            choice = (choice - 1) % 2
            hub.light_matrix.show_image(choices[choice])
        if hub.right_button.was_pressed():
            choice = (choice + 1 ) % 2
            hub.light_matrix.show_image(choices[choice])
        if hub.motion_sensor.was_gesture('tapped'):
            if choice == 1:
                hub.light_matrix.off()
                hub.speaker.beep(90, 0.15)
                hub.speaker.beep(94, 0.15)
                hub.speaker.beep(98, 0.15)
                return data
            if motor2:
                data[get_sensor_data()] = (motor.get_position(), motor2.get_position())
            else:
                data[get_sensor_data()] = motor.get_position()
            hub.light_matrix.show_image('YES')
            send({"training_data": data})
            hub.speaker.beep(90, 0.15)
            hub.speaker.beep(94, 0.15)
            choice = 0
            hub.light_matrix.show_image(choices[choice])

clamp = lambda n, minn, maxn: max(min(maxn, n), minn)

def proportional_adjust(target_angle, motor):
    error = target_angle - motor.get_position()
    power = floor(error*.8)
    power = clamp(power,-100,100)
    motor.start_at_power(power)


default = {
    (500, 0): 270,
    (500, 500): 180,
    (0,300): 90,
}

if motor2:
   default = {
        (500, 0): (270, 270),
        (500, 500): (180, 90),
        (0,300): (90, 270)
    } 


motor.run_to_position(180)
if motor2:
    motor2.run_to_position(180)
get_sensor_data = setup_get_sensor_data(color)

hub.motion_sensor.was_gesture('tapped')

train_flag = train_menu()
if train_flag:
    default = train(get_sensor_data, motor, motor2)

hub.light_matrix.off()
hub.light_matrix.show_image('DIAMOND')
rounds = 0

status = ["azure","blue","cyan","green","orange","pink","red","violet","yellow","white"]
while True:
    hub.status_light.on(status[rounds])
    current = get_sensor_data()
    send({"current_value": current})
    target_angle = choose(current, default)
    if motor2:
        proportional_adjust(target_angle[0], motor)
        proportional_adjust(target_angle[0], motor2)
    else:
        proportional_adjust(target_angle, motor)
#    motor.run_to_position(target_angle)
    rounds = (rounds + 1) % 10
    if rounds == 0:
        send({"training_data": default})
