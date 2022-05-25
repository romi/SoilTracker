## Motor control

### About

This part of the SoilTracker repository aims to deliver a proof of concept of the closed-loop capabilities of the robot, and to deliver some examples of how to control ROMI's motors.

### Closed-loop control solution

In order to be able to track the ground *so that the rotative tool will never be blocked by too much soil*, current measurements on the tool's motor are done. We are using a numeric model obtained through `digging_exp_protocol_2.py`. This model is adapted with a current measurement at a known depth as to increase fidelity.
A digital PI controller then reads the error at a certain instant and tries to minimize it by giving a certain input position that is added to the initial position, which is always equivalent to a tool that is 2cm deep in the ground.

### The model
Our model has been obtained through digging 20 times the same moat of soil and measuring the current on the tool's motor while tracking it's position along the Z-axis (i.e. its depth). After applying a fifth-order polynomial fit, we obtained a model that can associate a current measurement to an estimated depth at which the tool evolves.

### Pre-requisites

* odrive module
* matplotlib
* numpy
* scipy (for experimental **and highly bugged** current filters)
* colorama
* typing, dataclasses
