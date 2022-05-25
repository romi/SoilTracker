## Modules
import time
import numpy as np
import current_filter

## ODrive
import odrive
from odrive.enums import *
from odrive_utils import *

def calculateDepth(current, depthFunction, previousDepthError, previousUI):
    currentDepth = depthFunction( abs(current_filter.avg(current)) )            # update measure
    depthError = -2 - currentDepth
    Kp, Ki, Kd, Te = 0.45*6, 3.25/1.2, 0, 1/225                                 # Ki = 6, Tu = 3.25s

    ui = previousUI + (Ki * Te * depthError)                                    # update integral
    u = Kp * (depthError + ui + (Kd/Te)*(depthError - previousDepthError))      # update command
    print(f"currentDepth : {currentDepth:.2f}cm | depthError : {depthError:.2f}cm | correction : {u:.2f}cm")
    previousDepthError = depthError
    previousUI = ui
    return u * -grZ, previousDepthError, previousUI

## STEP 0 : DECLARE CONSTANTS
grZ = (22 + (2/3)) / 17                                                         # (rev/cm) : the tool translates 1 cm when the z-motor does gr revolution
grX = 1/4.4                                                                     # (rev/cm) : the z-axis translates 1 cm when the x-motor does gr revolution
obstacleMet = False                                                             # boolean value telling if an obstacle has been found
distLimitZ = 40                                                                 # value that indicates when to stop the motor if no obstacle has been found
currentThreshold = 1.3

## STEP 1 : POWER ON MOTORS
odrv0, odrv1 = get_odrv_objects()

if odrv0 != None and odrv1 != None:
    xAxis = odrv1.axis0
    zAxis = odrv0.axis0
    wAxis = odrv0.axis1
    allAxis = (xAxis, zAxis, wAxis)

power_on(odrv0)
power_on(odrv1)
print("STEP 1 : Motors are on")
time.sleep(3)

## STEP 2 : GROUND DETECTION
print("STEP 2 : Detecting ground")
zAxis.controller.config.input_mode = INPUT_MODE_PASSTHROUGH
startTime = time.time()                                                         # process start date
startZPosition = zAxis.encoder.pos_estimate                                     # start position
zPos = 0
zAxis.controller.config.vel_limit = 10
wAxis.controller.input_vel = 3                                                  # tool rotation
zAxis.controller.input_vel = 3                                                  # tool translation

currentWAxis = DataContainer()

while abs(zPos) <= distLimitZ and not obstacleMet:
    now = time.time()
    lateEnough = (now - startTime > 1.5)

    zRevolutions = zAxis.encoder.pos_estimate                                   # estimated position in revolutions
    zPos = (zRevolutions - startZPosition) / grZ                                # estimated position of the tool on the Z-axis

    # Update data
    currentWAxis.measure(abs(wAxis.motor.current_control.Iq_measured))

    if abs(currentWAxis.filtered[-1]) > currentThreshold and lateEnough:        # if current measured is greater than x amps
        print(f"Obstacle met on relative position z={zPos:.2f}cm!")
        obstacleMet = True

# Stopping the motor to its current position for the next process : going 2cm deep
zAxis.controller.config.control_mode = CONTROL_MODE_POSITION_CONTROL            # position control
zAxis.controller.input_pos = zAxis.encoder.pos_estimate                         # input position in revolutions
wAxis.controller.input_vel = 0                                                  # tool rotation

# cleanup
del currentWAxis
time.sleep(3)

## STEP 3 : GET THE CURRENT WHEN THE TOOL IS 2CM DEEP
print("STEP 3 : Getting offset between model and reality")

startZPosition = zAxis.encoder.pos_estimate                                     # start position
currentWAxis = DataContainer()

zAxis.controller.config.control_mode = CONTROL_MODE_VELOCITY_CONTROL            # position control
zAxis.controller.input_vel = 1                                                  # tool translation
wAxis.controller.input_vel = 10                                                 # tool rotation
zPos = 0
while (abs(zPos) <= 1.6):
    zRevolutions = zAxis.encoder.pos_estimate                                   # estimated position in revolutions
    zPos = (zRevolutions - startZPosition) / grZ                                # estimated position of the tool on the Z-axis
    # Update data
    currentWAxis.measure(abs(wAxis.motor.current_control.Iq_measured))

l = len(currentWAxis.filtered)
actualCurrent = current_filter.avg(currentWAxis.filtered[int(9.9*l/10):])

zAxis.controller.config.control_mode = CONTROL_MODE_POSITION_CONTROL            # position control
zAxis.controller.input_pos = zAxis.encoder.pos_estimate                         # input position in revolutions
# cleanup
del currentWAxis
time.sleep(3)

zAxis.controller.config.control_mode = CONTROL_MODE_POSITION_CONTROL            # position control
zAxis.controller.input_pos = zAxis.encoder.pos_estimate

## STEP 4 : DIG
print("Gardening beginning")
nominalDepthFunction = np.poly1d([-5.21187786e-03,  1.51010255e-01, -1.66762136e+00,  8.75482824e+00, -2.24501423e+01,  2.02731940e+01])
# /\ data acquired from
#  L previous experiments
actualDepth = -2
expectedDepth = nominalDepthFunction(actualCurrent)
offset = expectedDepth - actualDepth
depthFunction = nominalDepthFunction - offset

initialPosition = zAxis.encoder.pos_estimate
startXPosition = xAxis.encoder.pos_estimate

xAxis.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
xAxis.controller.config.control_mode = CONTROL_MODE_VELOCITY_CONTROL            # position control
xAxis.controller.input_vel = - 4 * grX                                          # tool translation : -4cm/s
zAxis.controller.config.control_mode = CONTROL_MODE_POSITION_CONTROL
zAxis.controller.config.input_mode = INPUT_MODE_POS_FILTER

currentWAxis = DataContainer()
prevDE, prevUI = 0, 0

mesConsigne = DataContainer()
mesPosition = DataContainer()
mesProfondeur = DataContainer()

while abs(xAxis.encoder.pos_estimate - startXPosition) / grX < 50:              # 50 cms is the length of our experimental terrain -> while the tool is in the workzone
    currentWAxis.measure(abs(wAxis.motor.current_control.Iq_measured))
    correction, prevDE, previUI = calculateDepth(currentWAxis.filtered[-50:], depthFunction, prevDE, prevUI)
    zAxis.controller.input_pos = initialPosition + correction
    mesConsigne.measure(zAxis.controller.input_pos)
    mesPosition.measure(zAxis.encoder.pos_estimate)
    mesProfondeur.measure(depthFunction( abs(current_filter.avg(currentWAxis.filtered[-50:])) ))

zAxis.controller.config.input_mode = INPUT_MODE_PASSTHROUGH
## STEP 5 : POWERING OFF MOTORS
print("Gardening ended")
power_off(odrv0)
power_off(odrv1)
