## Modules
import time
import numpy as np
import current_filter
from colorama import Back, Fore, Style

## ODrive
import odrive
from odrive.enums import *
from odrive_utils import *

## Variable declaration
# poulie menante : 34 ; poulie menée : 30
gr = -17 / (22 + (2/3))                                                         # the tool translates <gr> cm when the motor does 1 revolution
obstacle = False                                                                # boolean value telling if an obstacle has been found
dist_limit = 40                                                                 # value that indicates when to stop the motor if no obstacle has been found
current_threshold = 1.9
current_buffer = [[], []]

## Searching for an ODrive card + misc. code for readability
ERROR = Back.RED + Style.BRIGHT + " ERROR " + Style.RESET_ALL + " "
OK = Back.GREEN + Style.BRIGHT + " OK " + Style.RESET_ALL + " "
print(Fore.YELLOW + Style.BRIGHT + "Searching ODrive..." + Style.RESET_ALL)
try:
    odrv0 = odrive.find_any(serial_number="20533679424D")
    odrv1 = odrive.find_any(serial_number="367038563030") # X (& Y)
    print(Fore.GREEN + Style.BRIGHT + "ODrives linked!" + Style.RESET_ALL)
    print(OK + f"ODrive SN : {odrv0.serial_number}") # 20533679424D
    print(OK + f"ODrive SN : {odrv1.serial_number}") # 367038563030
except Exception as exc:
    print(exc)

time.sleep(1)

## Motor configuration : set motor velocity to 0 rpm
xAxis = odrv1.axis0
zAxis = odrv0.axis0
wAxis = odrv0.axis1
allAxis = (xAxis, zAxis, wAxis)

for ax in allAxis:
    ax.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL                         # ID : 8 ; closed loop control
    ax.controller.config.control_mode = CONTROL_MODE_VELOCITY_CONTROL           # velocity control
    ax.controller.input_vel = 0                                                 # input velocity in rps = (1/60)rpm

print("Initiating experiment : touching ground")
time.sleep(1)

## Ground detection + follow-up on position
pos = 0                                                                         # Relative end effector position variable
t_start = time.time()                                                           # time variable for the following loop's first iteration
start_time = time.time()                                                        # process start date
start_position = zAxis.encoder.pos_estimate                                     # start position

wAxis.controller.input_vel = 3                                                  # tool rotation
zAxis.controller.input_vel = 3                                                  # tool translation

while abs(pos) <= dist_limit and not obstacle:
    now = time.time()
    dt = now - t_start
    revolutions = zAxis.encoder.pos_estimate                                    # estimate position in revolutions
    pos = (revolutions - start_position) * gr
    # print(f"pos = {pos:.2f} cm, pos_estimate = {zAxis.encoder.pos_estimate: .4f}, t = {now - start_time: 0.6f}, dt = {dt: .6f}\t\t")
    t_start = now

    # Update buffers
    if len(current_buffer[0]) >= 5:
        current_buffer[0] = current_buffer[0][-4:]
    if len(current_buffer[1]) >= 5:
        current_buffer[1] = current_buffer[1][-4:]
    current_buffer[0].append(wAxis.motor.current_control.Iq_measured)
    current_buffer[1].append(zAxis.motor.current_control.Iq_measured)

    filtered_current = current_filter.avg(current_buffer[0])

    if abs(filtered_current) > current_threshold and now-start_time > 1.5:      # if current measured is greater than x amps
        print(f"Obstacle met on relative position z={pos:.2f}cm!")
        obstacle = True

# Stopping the motor for the next process : going 2cm deep
zAxis.controller.config.control_mode = CONTROL_MODE_POSITION_CONTROL            # position control
zAxis.controller.input_pos = zAxis.encoder.pos_estimate                         # input position in revolutions
wAxis.controller.input_vel = 0                                                  # tool rotation

time.sleep(5)

print("Going deep")
wAxis.controller.input_vel = 3

if zAxis.encoder.pos_estimate < start_position:
    # going deep means adding a certain value to the input position
    two_cm_deep = 2 / gr
else:
    # going deep means substracting a certain value to the input position
    two_cm_deep = - 2 / gr

# Going 2cm deep in the soil
zAxis.controller.input_pos += two_cm_deep

### STARTING THE 2nd EXPERIMENT
print("Now let's garden!")
start_position_x = xAxis.encoder.pos_estimate

# Going forward
xAxis.controller.input_vel = -1

current_buffers_2 = [[], [], []]
current_data_2 = [[], [], []]
time_2 = []

t_start_2 = time.time()
while abs(xAxis.encoder.pos_estimate - start_position_x) < 9.5:
    # Gather and filter data
    now = time.time()
    dt = now - t_start_2

    for i, buffer in enumerate(current_buffers_2):
        if len(buffer) >= 5:                                                    # getting the last 5 current values of each motor
            buffer = buffer[-4:]
        buffer.append(allAxis[i].motor.current_control.Iq_measured)
        current_value = current_filter.avg(buffer)                              # average filter
        current_buffers_2[i] = buffer                                           # update buffers
        current_data_2[i].append(current_value)                                 # saving data
    time_2.append(dt)

print("Gardening ended")
power_off(odrv0)
power_off(odrv1)

# Saving data
SAVE_PATH = "ExpData/CurrentWhileGardening/"
np.savetxt(SAVE_PATH+"xAxis.txt", current_data_2[0])
np.savetxt(SAVE_PATH+"zAxis.txt", current_data_2[1])
np.savetxt(SAVE_PATH+"wAxis.txt", current_data_2[2])
np.savetxt(SAVE_PATH+"time.txt", time_2)
