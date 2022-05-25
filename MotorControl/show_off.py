### SERIAL NUMBERS
# X & Y : 367038563030
# Z & W : 367138573030 // 20533679424D (dead) // 206A3371304B (dead)

import odrive
from odrive.enums import *
from odrive_utils import *
import numpy as np
import time as t

print("Starting initialization")

odrv0 = odrive.find_any(serial_number="367138573030") # Z & W
odrv1 = odrive.find_any(serial_number="367038563030") # X (& Y)

xAxis = odrv1.axis0
zAxis = odrv0.axis1
wAxis = odrv0.axis0
allAxis = (xAxis, zAxis, wAxis)

## Motor configuration : set motor velocity to 0 rpm
for ax in allAxis:
    ax.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL                         # ID : 8 ; closed loop control
    ax.controller.config.control_mode = CONTROL_MODE_VELOCITY_CONTROL           # velocity control
    ax.controller.input_vel = 0                                                 # input velocity in rps = (1/60)rpm

# start & end positions for showoff procedure. HAS TO BE CHANGED ON EACH REBOOT
# x, z, w
revStart = [2.343874931335449, 0.0012421038700267673, -0.02038281224668026]
revEnd = [-7.517382621765137, 0.0005155196413397789, -0.02038281224668026]

xAxis.controller.config.vel_limit = 2
zAxis.controller.config.vel_limit = 6

xAxis.controller.config.control_mode = CONTROL_MODE_POSITION_CONTROL
zAxis.controller.config.control_mode = CONTROL_MODE_POSITION_CONTROL

for (i, ax) in enumerate(allAxis):
    ax.controller.input_pos = revStart[i]

time.sleep(10)
print("Starting Showoff")

xAxis.controller.input_pos = revEnd[0]
wAxis.controller.input_vel = 2

tStart = time.time()
while abs(xAxis.encoder.pos_estimate) < 7.5:
    tNow = time.time() - tStart
    zAxis.controller.input_pos = np.sin(np.pi * 2 * tNow)
    time.sleep(0.1)

xAxis.controller.config.vel_limit = 10
zAxis.controller.config.vel_limit = 10

print("Ending Showoff")

power_off(odrv0)
power_off(odrv1)
