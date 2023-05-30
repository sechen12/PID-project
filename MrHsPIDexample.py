#My Name is Optimus Prime
#The autobots and I fled our world


import time #import files
import board
import pwmio
import rotaryio
import analogio
import pulseio
import digitalio
import simpleio
from adafruit_motor import motor
from PID_CPY import PID
from analogio import AnalogOut, AnalogIn
from digitalio import DigitalInOut, Direction, Pull

AIN1 = pwmio.PWMOut(board.D7,duty_cycle=2 ** 20, frequency=40) #motor ouput
AIN2 = pwmio.PWMOut(board.D6,duty_cycle=2 ** 20, frequency=40)
BIN1 = pwmio.PWMOut(board.D9,duty_cycle=2 ** 20, frequency=40)
BIN2 = pwmio.PWMOut(board.D8,duty_cycle=2 ** 20, frequency=40)

motor1 = motor.DCMotor(AIN1,AIN2)
motor2 = motor.DCMotor(BIN1,BIN2)

encoder = rotaryio.IncrementalEncoder(board.D1, board.D2)
last_position = 0
btn = DigitalInOut(board.D3)
btn.direction = Direction.INPUT
btn.pull = Pull.UP
state = 0
delta = 1   
photoVal = False           
oldPhotoVal = False # Used to make sure we only count the first loop when interupt is broken   

photoint = DigitalInOut(board.D11) #identify photointerrupter
photoint.pull =Pull.UP #pull up photointerrupter
previous_time = 0.0
current_time = 1.0 
time_diff = 0.0
time_diff = current_time - previous_time
rpmCheckTime = 0.0
rpmCheckState = True
rpm = 0

pid = PID(1,0.1,0.05, setpoint=100)
#pid.sample_time = 0.1
pid.output_limits = (0,None)

while True:
    
    photoVal = photoint.value
    
    if time.monotonic() > rpmCheckTime + 0.5:
        rpmCheckState = not rpmCheckState
        print(rpmCheckState)
        previous_time = time.monotonic()
        rpmCheckTime = previous_time
        

    if rpmCheckState:
        if  not photoVal and oldPhotoVal: 
            current_time = time.monotonic()
            time_diff = current_time - previous_time + 0.1
            #Speed = Distance / Time
            rpm = (8.0/time_diff) * 60
            time.sleep(.0)
            
    else:
        control = pid(rpm)
        print("RPM: " + str(rpm), "TIme Diff: " + str(time_diff))
        position = encoder.position
        if position != last_position:
            if position > last_position:
                state = state + 1
            elif position < last_position:
                state = state - 1
            if state > 0:
                print("Enocder: " + str(state))
                motor1.throttle = int(simpleio.map_range(state,1,20,0,65535)) / -65535
                motor2.throttle = int(simpleio.map_range(state,1,20,0,65535)) / -65535
                print("Motor Value: " + str(simpleio.map_range(state,1,10,0,65535)))
                time.sleep(0.5)
            if state < 0:
                motor1.throttle = control
                motor2.throttle = control
                print("Motor Value: " + str(control))
        if btn.value == 1:
            time.sleep(.5)
            delta = 1
            
        last_position = position
    oldPhotoVal = photoVal
    previous_time = current_time
