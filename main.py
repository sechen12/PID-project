import time
import board
import analogio as AIO
import digitalio as DIO
from lcd.lcd import LCD
from lcd.i2c_pcf8574_interface import I2CPCF8574Interface

# i2c = board.I2C()
# lcd = LCD(I2CPCF8574Interface(i2c, 0x3f), num_rows=2, num_cols=16)

inter = DIO.DigitalInOut(board.D11)
inter.direction = DIO.Direction.INPUT
inter.pull = DIO.Pull.UP

kp = .5
ki = .02
kd = .02
prevPoint =0
input = 0
setPoint = 50
output = 0
integral =0
lastError =0
dt =.01

val=0

def compute():
    global output,integral
    output += (kp * (setPoint - input))
    integral += (setPoint - input) * time.process_time()
    output += (ki * integral)
    output += kd * ((setPoint - input) - lastError / time.process_time())
    return output

interupts =0
time1 = 0
time2 = 0
rpms = 0
lastVal = False

while True: 
    compute()
    if inter.value and lastVal == False:
        lastVal = True
        interupts += 1
    else:
        lastVal  = False

    if interupts %2 == 0:
        time1 = time.monotonic()
    if interupts %2 == 1:
        time2 = time.monotonic()
        rpms = round((time2 - time1)*60,2)


    print(f"{inter.value} ")


