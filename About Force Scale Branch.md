**This is a small readme to explain briefly the codes in Force Scale branch.**

*CalibrationAnalyse.py & CalibrationProcess.py*
These codes are for calibration : We collect a 1000 weight mesures for each of the 10 random objects scaled. We put all the data in text files to then extract them in the second 
code. We approximate the relation between weight and voltage with a linear regression, to finally plot the result. We also plot the standard deviation of each scale.

*Force_mesures_live.py*
This code is for live plotting of "real time" measured weights. We'll convert them to a Force, to approach the efforts applied by the weeder robot's arm. 
Which will enable us to estimate the needed torque to weed a special soil. 
