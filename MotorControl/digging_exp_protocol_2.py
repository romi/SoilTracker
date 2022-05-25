## Modules
import time
import numpy as np
import current_filter

## ODrive
import odrive
from odrive.enums import *
from odrive_utils import *

## Misc
import os, sys

SAVE_PATH = "ExpData/CurrentDepthLaw/"
prefixes = ("currentZAxis_dig", "currentWAxis_dig", "velWAxis_dig", "posZ_dig")

grZ = -17 / (22 + (2/3))                                                        # (cm/rev) : the tool translates <grZ> cm when the z-motor does 1 revolution
grX = 4.4                                                                       # (cm/rev) : the z-axis translates <grX> cm when the x-motor does 1 revolution

odrv0, odrv1 = get_odrv_objects()
odrvs = (odrv0, odrv1)

if odrv0 != None and odrv1 != None:
    xAxis = odrv1.axis0
    zAxis = odrv0.axis1
    wAxis = odrv0.axis0
    allAxis = (xAxis, zAxis, wAxis)
else:
    ERROR = Back.RED + Style.BRIGHT + " ERROR " + Style.RESET_ALL + " "
    print(f"{ERROR} ODrive objects not initialized properly")

input("Place the robot correctly and press enter to begin")
power_on(odrv0)
power_on(odrv1)

## Placing the robot in the middle of the terrain
startPositionX = xAxis.encoder.pos_estimate

xAxis.controller.input_vel = -2
while abs(xAxis.encoder.pos_estimate - startPositionX) * grX < 30: # the tool will go 30cm "forwards"
    continue

xAxis.controller.config.control_mode = CONTROL_MODE_POSITION_CONTROL
xAxis.controller.input_pos = xAxis.encoder.pos_estimate

## Ground detection + follow-up on position
obstacleMet = False                                                             # boolean value telling if an obstacle has been found
distLimitZ = 40                                                                 # value that indicates when to stop the motor if no obstacle has been found
currentThreshold = 1.5
pos = 0                                                                         # Relative end effector position variable
startTime = time.time()                                                         # process start date
startZPosition = zAxis.encoder.pos_estimate                                     # start position

wAxis.controller.input_vel = 3                                                  # tool rotation
zAxis.controller.input_vel = 3                                                  # tool translation

currentWAxis = DataContainer()
currentZAxis = DataContainer()

while abs(pos) <= distLimitZ and not obstacleMet:
    now = time.time()
    lateEnough = (now - startTime > 1.5)

    zRevolutions = zAxis.encoder.pos_estimate                                   # estimated position in revolutions
    zPos = (zRevolutions - startZPosition) * grZ                                # estimated position of the tool on the Z-axis

    # Update data
    currentWAxis.measure(wAxis.motor.current_control.Iq_measured)
    currentZAxis.measure(zAxis.motor.current_control.Iq_measured)

    if abs(currentWAxis.filtered[-1]) > currentThreshold and lateEnough:        # if current measured is greater than x amps
        print(f"Obstacle met on relative position z={zPos:.2f}cm!")
        obstacleMet = True

zAxis.controller.config.control_mode = CONTROL_MODE_POSITION_CONTROL            # position control
zAxis.controller.input_pos = zAxis.encoder.pos_estimate                         # input position in revolutions
wAxis.controller.input_vel = 0                                                  # tool rotation
time.sleep(2)

print("Going up")
if zAxis.encoder.pos_estimate > startZPosition:
    # going deep means adding a certain value to the input position
    fiveCmUp = 5 / grZ
else:
    # going deep means substracting a certain value to the input position
    fiveCmUp = - 5 / grZ

xAxis.controller.config.control_mode = CONTROL_MODE_POSITION_CONTROL
xAxis.controller.input_pos = xAxis.encoder.pos_estimate
zAxis.controller.input_pos += fiveCmUp

del currentWAxis
del currentZAxis

time.sleep(1.5)
print("Beginning experiment!")
time.sleep(1.5)

## Initiate digging
for i in range(1, 21):
    print(f"Beginning iteration {i}")
    depth = zAxis.encoder.pos_estimate - (5/grZ)
    currentZAxis_dig = DataContainer()
    currentWAxis_dig = DataContainer()
    velWAxis_dig = DataContainer()
    posZ_dig = DataContainer()
    datasets = (currentZAxis_dig, currentWAxis_dig, velWAxis_dig, posZ_dig)
    startPositionZ = zAxis.encoder.pos_estimate

    stopCondition = False
    zAxis.controller.config.control_mode = CONTROL_MODE_VELOCITY_CONTROL
    zAxis.controller.input_vel = -2 * grZ
    wAxis.controller.input_vel = 10

    while abs((zAxis.encoder.pos_estimate - startPositionZ) * grZ) < 25 and stopCondition == False: # the tool will (try to) go 25cm deep
        currentZAxis_dig.measure(zAxis.motor.current_control.Iq_measured)
        currentWAxis_dig.measure(wAxis.motor.current_control.Iq_measured)
        current_overload = (abs(current_filter.avg(currentZAxis_dig.filtered[-150:])) > 6.5)
        zRevolutions = zAxis.encoder.pos_estimate                                   # estimated position in revolutions
        zPos = (zRevolutions - depth) * grZ                                         # estimated position of the tool on the Z-axis1
        posZ_dig.measure(zPos)
        velWAxis_dig.measure(wAxis.encoder.vel_estimate)
        if current_overload or len(currentZAxis_dig.t) > 20_000:
            if currentZAxis_dig.t[-1] > 1:
                stopCondition = True

    zAxis.controller.config.control_mode = CONTROL_MODE_POSITION_CONTROL
    zAxis.controller.input_pos = startPositionZ
    while abs((zAxis.encoder.pos_estimate - startPositionZ) * grZ) > 0.1: # the tool will return to its start position
        continue
    print(f"Iteration {i} ended, saving..\nRebuild the terrain")
    wAxis.controller.input_vel = 0
    it = "Iteration%02d/" % i
    for prefix, data in zip(prefixes, datasets):
        data.save(SAVE_PATH+it+prefix)
    time.sleep(35)
    for i in range(10):
        print("\r\007", end="")                                                 # alarm
        time.sleep(0.1)
    time.sleep(4)
