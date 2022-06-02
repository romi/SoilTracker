## Modules
import time
import numpy as np
import current_filter

## ODrive
import odrive
from odrive.enums import *
from odrive_utils import *

## Variable declaration
# poulie menante : 34 ; poulie menée : 30
grZ = -17 / (22 + (2/3))                                                        # (cm/rev) : the tool translates <grZ> cm when the z-motor does 1 revolution
grX = 4.4                                                                       # (cm/rev) : the z-axis translates <grX> cm when the x-motor does 1 revolution
obstacleMet = False                                                             # boolean value telling if an obstacle has been found
distLimitZ = 40                                                                 # value that indicates when to stop the motor if no obstacle has been found
currentThreshold = 1.5

## Assigning ODrive cards to an interface

odrv0, odrv1 = get_odrv_objects()
odrvs = (odrv0, odrv1)

if odrv0 != None and odrv1 != None:
    xAxis = odrv1.axis0
    zAxis = odrv0.axis0
    wAxis = odrv0.axis1
    allAxis = (xAxis, zAxis, wAxis)
else:
    ERROR = Back.RED + Style.BRIGHT + " ERROR " + Style.RESET_ALL + " "
    print(f"{ERROR} ODrive objects not initialized properly")

time.sleep(1)

## Motor configuration : set motor velocity to 0 rpm

for odrv in odrvs:
    power_on(odrv)

print("Initiating experiment : touching ground")
time.sleep(1)

## Ground detection + follow-up on position
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

# Stopping the motor for the next process : going 2cm deep
zAxis.controller.config.control_mode = CONTROL_MODE_POSITION_CONTROL            # position control
zAxis.controller.input_pos = zAxis.encoder.pos_estimate                         # input position in revolutions
wAxis.controller.input_vel = 0                                                  # tool rotation

time.sleep(5)

# Going forward
xOffset = float(input("Please enter the offset between the tool's\ncurrent position and the pot's left border (cm) >>> "))

print("Going deep")
wAxis.controller.input_vel = 6
if zAxis.encoder.pos_estimate < startZPosition:
    # going deep means adding a certain value to the input position
    twoCmDeep = 2 / grZ
else:
    # going deep means substracting a certain value to the input position
    twoCmDeep = - 2 / grZ

# Going 2cm deep in the soil
zAxis.controller.input_pos += twoCmDeep

### STARTING THE 2nd EXPERIMENT
print("Now let's garden!")

currentXAxis = DataContainer()
currentZAxis = DataContainer()
currentWAxis = DataContainer()
velWAxis = DataContainer()
velXAxis = DataContainer()

startXPosition = xAxis.encoder.pos_estimate                                     # start position
xIndex = []

xAxis.controller.input_vel = -1
while xOffset + abs(xAxis.encoder.pos_estimate - startXPosition)*grX < 58:      # 58 cms is the length of our experimental terrain -> while the tool is in the workzone
    # Gather and filter data
    xRevolutions = xAxis.encoder.pos_estimate                                   # estimated position in revolutions
    xPos = xOffset + abs(xRevolutions - startXPosition) * grX                   # estimated tool position on the workzone
    xIndex.append(xPos)

    currentXAxis.measure(xAxis.motor.current_control.Iq_measured)
    currentZAxis.measure(zAxis.motor.current_control.Iq_measured)
    currentWAxis.measure(wAxis.motor.current_control.Iq_measured)
    velWAxis.measure(wAxis.encoder.vel_estimate)
    velXAxis.measure(xAxis.encoder.vel_estimate)

print("Gardening ended")
power_off(odrv0)
power_off(odrv1)

# Saving data

# terrainProfile = [ [0, 6, 12, 18, 21, 22, 24, 26, 28, 30, 31, 35, 37, 38, 40, 42, 44, 45, 46, 47, 48, 49, 50, 52, 54, 56, 60, 67],
#                     [7, 7, 7, 7, 7, 8, 9, 10, 11, 12.5, 14, 14, 14, 13, 12, 11, 10, 9, 8, 7, 6.5, 6, 5, 4.5, 4, 3, 3, 3]]
# current while gardening, exp 1 à 5 & success 1 à 3

# terrainProfile = [[i for i in np.arange(0, 70.1, 0.1)], [16-8.5 for i in np.arange(0, 40.1, 0.1)] + [16 -(8.5 - i*(6/30)) for i in np.arange(0.1, 30.1, 0.1)]]

terrainProfile = [
    [0, 6, 12, 18, 25, 26, 27, 28, 29, 30, 32, 34, 35, 40, 45, 46, 47, 49, 50, 51, 52, 53, 54, 60, 67],
    [2, 2, 2, 2, 2, 3.5, 4, 4.5, 5.5, 6, 7, 8, 8.5, 8.5, 8.5, 8, 7, 5, 4, 3.5, 3, 2.5, 1.5, 1.5, 1.5]
]


# 1st element : x indexes, 2nd element : depth (cm)
# tip : plt.axis("scaled") when displaying the terrain's profile in order to have something that looks like the real thing

SAVE_PATH = "ExpData/DataCollectionProject/Iteration10/"
currentXAxis.save(SAVE_PATH+"currentXAxis")
currentZAxis.save(SAVE_PATH+"currentZAxis")
currentWAxis.save(SAVE_PATH+"currentWAxis")
velXAxis.save(SAVE_PATH+"velXAxis")
velWAxis.save(SAVE_PATH+"velWAxis")
np.savetxt(SAVE_PATH+"xIndex.txt", xIndex)
np.savetxt(SAVE_PATH+"tStart.txt", [currentWAxis.t_start])
print(currentWAxis.t_start)
