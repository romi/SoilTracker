import odrive
import time
import os
import matplotlib.pyplot as plt
import numpy as np
from colorama import Back, Fore, Style
from datetime import datetime
from matplotlib.animation import FuncAnimation
from odrive_variables import *
from current_filter import *

ERROR = Back.RED + Style.BRIGHT + " ERROR " + Style.RESET_ALL + " "
OK = Back.GREEN + Style.BRIGHT + " OK " + Style.RESET_ALL + " "

def animate(i, xs, ys, buffer, yraw):
    try:
        # Update buffers so that they contain the 5 last values
        if len(buffer[0]) >= 5:
            buffer[0] = buffer[0][-4:]
        if len(buffer[1]) >= 5:
            buffer[1] = buffer[1][-4:]
        buffer[0].append(odrv0.axis0.motor.current_control.Iq_measured)
        buffer[1].append(odrv0.axis1.motor.current_control.Iq_measured)
        yraw[0].append(odrv0.axis0.motor.current_control.Iq_measured)
        yraw[1].append(odrv0.axis1.motor.current_control.Iq_measured)

        # Add x and y to lists
        xs.append(datetime.now())
        ys[0].append(avg(buffer[0]))
        ys[1].append(avg(buffer[1]))
        xs2 = xs[-50:]
        ys20 = ys[0][-50:]
        ys21 = ys[1][-50:]

        # Draw x and y lists
        ax.clear()
        ax.plot(xs2, ys20)
        ax.plot(xs2, ys21)

        # Format plot
        plt.xticks(rotation=45, ha='right')
        plt.subplots_adjust(bottom=0.30)
        plt.title('Current over time')
        plt.ylabel('Current (amps)')
    except KeyboardInterrupt:
        os.exit()
    return

# Find ODrive
print(Fore.YELLOW + Style.BRIGHT + "Searching ODrive..." + Style.RESET_ALL)
try:
    odrv0 = odrive.find_any()
    print(Fore.GREEN + Style.BRIGHT + "ODrive linked!" + Style.RESET_ALL)
except Exception as exc:
    print(ERROR)
    print(exc)
    os.exit()

print(OK + f"ODrive SN : {odrv0.serial_number}")

# Configure axis for closed loop control on velocity
odrv0.axis1.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL                    # ID : 8 ; closed loop control
odrv0.axis1.controller.config.control_mode = CONTROL_MODE_VELOCITY_CONTROL      # on velocity
odrv0.axis1.controller.input_vel = 2                                            # velocity reference

print("Starting liveplot")

# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs, ys = [], [[], []]
yraw = [[], []]
buffer = [[], []]

# Display plot
ani = FuncAnimation(fig, animate, fargs=(xs, ys, buffer, yraw), interval=10)
plt.show()

np.savetxt("current_data_raw.txt", yraw)
np.savetxt("current_data_filtered.txt", ys)

odrv0.axis1.controller.input_vel = -2
time.sleep(1.5)
odrv0.axis1.controller.input_vel = 0
