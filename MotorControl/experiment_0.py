# copy-paste in an odrivetool session
# Experiment 0 : we plot the current measured on the Z-axis motor when it moves a
# certain mass vertically.
#
# Objective : determine a link between the current drawn by the Z-axis motor
# and the mass it has to displace.
#
# Results : Indeed, the greater the mass, the greater the current drawn.
# This comes from [torque] = [torque_constant] * [current]
# When a mass is subject to gravity, it creates a resistive torque on the Z-axis
# motor shaft, which has to be compensated by the motor when it is given a
# reference velocity through odrv0.axis0.controller.input_vel.
#
# This experiment allowed us to underline the need of a gearbox for the Z-axis
# motor, as the current necessary to move the hoe is quite high (27 amps)

import pandas as pd
import matplotlib.pyplot as plt
import time as t

df = pd.DataFrame(columns = ["t", "I"])
tstart = t.time()

# measuring current when the motor has to maintain its current position
for i in range(80):
    mot_current = odrv0.axis0.motor.current_control.Iq_measured
    df = df.append({"t": t.time() - tstart, "I": mot_current}, ignore_index = True)
    t.sleep(0.05)

odrv0.axis0.controller.input_vel = 0.7

# measuring current when the motor has to fight against gravity
for i in range(160):
    mot_current = odrv0.axis0.motor.current_control.Iq_measured
    df = df.append({"t": t.time() - tstart, "I": mot_current}, ignore_index = True)
    t.sleep(0.05)

odrv0.axis0.controller.input_vel = 0

# exporting the data for later use
df.to_csv("output.csv")
df.plot(kind="line", x="t", y="I")
