## Modules
import time
import numpy as np
import current_filter

## ODrive
import odrive
from odrive.enums import *
from odrive_utils import *

grZ = -17 / (22 + (2/3))                                                        # (cm/rev) : the tool translates <grZ> cm when the z-motor does 1 revolution
grX = 4.4                                                                       # (cm/rev) : the z-axis translates <grX> cm when the x-motor does 1 revolution
input("Press enter to start measurements")

odrv0, odrv1 = get_odrv_objects()
odrvs = (odrv0, odrv1)
power_on(odrv0)
power_on(odrv1)

if odrv0 != None and odrv1 != None:
    xAxis = odrv1.axis0
    zAxis = odrv0.axis1
    wAxis = odrv0.axis0
    allAxis = (xAxis, zAxis, wAxis)
else:
    ERROR = Back.RED + Style.BRIGHT + " ERROR " + Style.RESET_ALL + " "
    print(f"{ERROR} ODrive objects not initialized properly")

## Unloaded xAxis
currentXAxis = DataContainer()
startPositionX = xAxis.encoder.pos_estimate

xAxis.controller.input_vel = -0.5
while abs(xAxis.encoder.pos_estimate - startPositionX) * grX < 60: # the tool will go 60cm "forwards"
    currentXAxis.measure(xAxis.motor.current_control.Iq_measured)

xAxis.controller.config.control_mode = CONTROL_MODE_POSITION_CONTROL
xAxis.controller.input_pos = startPositionX

## Unloaded zAxis
currentZAxis = DataContainer()
startPositionZ = zAxis.encoder.pos_estimate

zAxis.controller.input_vel = -0.5 * grZ
while abs((zAxis.encoder.pos_estimate - startPositionZ) * grZ) < 25: # the tool will go 25cm deep
    currentZAxis.measure(zAxis.motor.current_control.Iq_measured)

zAxis.controller.config.control_mode = CONTROL_MODE_POSITION_CONTROL
zAxis.controller.input_pos = startPositionZ

## Unloaded wAxis
currentWAxis = DataContainer()

wAxis.controller.input_vel = 6
currentWAxis.measure(wAxis.motor.current_control.Iq_measured)
while currentWAxis.t[-1] < 30: # the tool will go 60cm "forwards"
    currentWAxis.measure(wAxis.motor.current_control.Iq_measured)


power_off(odrv0)
power_off(odrv1)
