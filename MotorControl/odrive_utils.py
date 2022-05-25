from dataclasses import dataclass, field
from typing import List
from odrive.enums import *
from colorama import Fore, Style, Back

import odrive
import time
import current_filter
import numpy as np
# https://github.com/odriverobotics/ODrive/blob/fw-v0.4.12/docs/encoders.md

@dataclass
class DataContainer:
    raw: List[float] = field(default_factory=lambda:[])
    filtered: List[float] = field(default_factory=lambda:[])
    t: List[float] = field(default_factory=lambda:[])
    buffer_size: int = 80
    t_start: float = 0.0
    first_measure: bool = True

    # TODO : make it so accoridng to the filter selected, the function does not have to be changed
    # IDEA : make a function filterWrapper(filter_func, arg_list) that invokes filter_func with the corresponding args
    def measure(self, data, filter=current_filter.avg):
        if (self.first_measure):
            self.t_start = time.time()
            self.first_measure = False
        self.t.append(time.time() - self.t_start)
        self.raw.append(data)
        self.filtered.append(filter(self.raw[-self.buffer_size:]))              # test filter

    def save(self, prefix):
        np.savetxt(f"{prefix}_raw.txt", self.raw)
        np.savetxt(f"{prefix}_filtered.txt", self.filtered)
        np.savetxt(f"{prefix}_time.txt", self.t)

def pause(t = 0.1):
    """
    there is not much about this function
    """
    print("Pause started")
    time.sleep(t)
    print("Pause ended")
    return None

# TODO : allow for customization of these parameters. This function is set to
# work with a certain motor.
def configure_motor(target_serial_number, axis_id = 0):
    """
    Function that configures the ODrive card to function with the motor
    /!\ execution is long (60 seconds)
    /!\ calibration must be done with the motor not connected to anything
    """
    odrv = odrive.find_any(serial_number = target_serial_number)
    if axis_id == 0:
        axis = odrv.axis0
    else:
        axis = odrv.axis1

    odrv.config.enable_brake_resistor = True
    odrv.config.brake_resistance = 2                                            # 50W2RJ resistor plugged to AUX on the ODrive
    axis.controller.config.vel_limit = 10                                       # rps limit
    axis.motor.config.pole_pairs = 7                                            # Datasheet extracted value
    axis.motor.config.torque_constant = 8.27/270                                # Motor K_v = 270 rpm/V
    axis.motor.config.motor_type = 0                                            # MOTOR_TYPE_HIGH_CURRENT since we're using a BLDC.
    axis.encoder.config.cpr = 2000                                              # Counts per revolution. cf. AMT102-V datahsheet, DIP Switch
    pause(2)
    axis.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE                 # Motor calibration state
    pause(20)
    axis.encoder.config.use_index = True                                        # We're using the encoder's Z output to calibrate the latter through stored index
    axis.requested_state = AXIS_STATE_ENCODER_INDEX_SEARCH                      # The motor will turn until it finds the index
    pause(20)
    axis.requested_state = AXIS_STATE_ENCODER_OFFSET_CALIBRATION                # Then it will calibrate
    pause(20)
    axis.encoder.config.pre_calibrated = True                                   # Boolean values indicating everything is calibrated for future uses
    axis.config.startup_encoder_index_search = True
    axis.motor.config.pre_calibrated = True
    odrv.save_configuration()                                                   # We're saving the configuration
    return None

def power_on(odrv_object):
    """
    Function that powers on the system. Specifically, it enables closed loop
    control on both motors and commands them to maintain 0 rpm
    """
    axis = (odrv_object.axis0, odrv_object.axis1)
    for ax in axis:
        ax.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
        ax.controller.config.control_mode = CONTROL_MODE_VELOCITY_CONTROL
        ax.controller.input_vel = 0
    return None

def power_off(odrv_object):
    """
    Function that powers down the system. Specifically, it disables closed loop
    control on both motors and sets them to an idle state
    """
    axis = (odrv_object.axis0, odrv_object.axis1)
    for ax in axis:
        ax.controller.input_vel = 0                                             #
        ax.controller.input_pos = ax.encoder.pos_estimate                       # ensures that on power on, the motors won't go to a faraway position
        ax.requested_state = AXIS_STATE_IDLE
    return None

def get_odrv_objects():
    ERROR = Back.RED + Style.BRIGHT + " ERROR " + Style.RESET_ALL + " "
    OK = Back.GREEN + Style.BRIGHT + " OK " + Style.RESET_ALL + " "
    print(Fore.YELLOW + Style.BRIGHT + "Searching ODrive..." + Style.RESET_ALL)
    try:
        odrv0 = odrive.find_any(serial_number="367138573030") # Z & W
        odrv1 = odrive.find_any(serial_number="367038563030") # X (& Y)
        print(Fore.GREEN + Style.BRIGHT + "ODrives linked!" + Style.RESET_ALL)
        print(OK + f"ODrive SN : {odrv0.serial_number}") # 20533679424D
        print(OK + f"ODrive SN : {odrv1.serial_number}") # 367038563030
    except Exception as exc:
        print(exc)
        return None, None
    return odrv0, odrv1
