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
zAxis = odrv0.axis0
wAxis = odrv0.axis1
allAxis = (xAxis, zAxis, wAxis)

## Motor configuration : set motor velocity to 0 rpm
power_on(odrv0)
power_on(odrv1)

# start & end positions for showoff procedure. HAS TO BE CHANGED ON EACH REBOOT
# x, z, w
revStart = [5.891118049621582,
            -12.116500854492188,
            56.85087585449219]

revEnd = [  -6.251624584197998,
            -12.116500854492188,
            56.85011672973633]


xAxis.controller.config.vel_limit = 2
zAxis.controller.config.vel_limit = 20

xAxis.controller.config.control_mode = CONTROL_MODE_POSITION_CONTROL
zAxis.controller.config.control_mode = CONTROL_MODE_POSITION_CONTROL

for (i, ax) in enumerate(allAxis):
    ax.controller.input_pos = revStart[i]

time.sleep(10)
print("Starting Showoff")

xAxis.controller.config.control_mode = CONTROL_MODE_VELOCITY_CONTROL
xAxis.controller.input_vel = -1.5

tStart = time.time()
while abs(xAxis.encoder.pos_estimate - revEnd[0]) > 0.1:
    tNow = time.time() - tStart
    zAxis.controller.input_pos += 5 * np.sin(tNow * 2 * np.pi)
    wAxis.controller.input_vel = xAxis.encoder.pos_estimate
    time.sleep(0.1)

xAxis.controller.config.vel_limit = 10
zAxis.controller.config.vel_limit = 10

print("Ending Showoff")

power_off(odrv0)
power_off(odrv1)
