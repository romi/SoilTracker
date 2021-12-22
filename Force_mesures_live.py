from Phidget22.Phidget import *
from Phidget22.Devices.VoltageRatioInput import *

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from matplotlib.pyplot import figure
import time 
from datetime import datetime 

MasseMax = 5 #kg
Max_N_Data = 15 #Data to display before "moving the window"

#Set up the figure, axis 
Pw = plt.figure(figsize=(10,10))
x = []
y = []
plt.grid()
plt.xlabel("Time(s)")
plt.ylabel("Weight(g)")
plt.title("Force mesures")
plt.ylim(0.0, 5000.0)
line, = plt.plot([],[],'m')

File = open("WeightExperiment.txt","w")
		
#Converts Voltage Ratio to weight
def ConvertVoltage(voltage0,voltage1,voltage2) :  
	#Slope and intercept values
	fichier = open("LinearRegression.txt","r")
	slope = float(fichier.readline().strip())
	intercept = float(fichier.readline().strip())
	fichier.close()
	
	#Write the weights mesured
	
	weight = slope*(voltage0+voltage1+voltage2) + 3*intercept
	
	if weight < 0 :
		File.write("0.0 grammes\n")
		return 0
	else :
		File.write(str(weight)+" grammes\n")
		return weight
	
	

	
def animate(self) :
	#Creat the three objects 
	Input0 = VoltageRatioInput()
	Input1 = VoltageRatioInput()
	Input2 = VoltageRatioInput()
	#Precise the channel 
	Input0.setChannel(0)
	Input1.setChannel(1)
	Input2.setChannel(2)
	#Reads the port
	Input0.openWaitForAttachment(100)
	Input1.openWaitForAttachment(100)
	Input2.openWaitForAttachment(100)
	#reads the voltage Ratio
	voltageRatio0 = Input0.getVoltageRatio()
	voltageRatio1 = Input1.getVoltageRatio()
	voltageRatio2 = Input2.getVoltageRatio()
	
	
	x.append(datetime.now())
	y.append(ConvertVoltage(voltageRatio))
	
	if len(x) > Max_N_Data :
		x.pop(0)
		y.pop(0)
	
	line.set_data(x,y)
		
	Pw.gca().relim()
	Pw.gca().autoscale_view(tight = True)
	
	return line

anim = animation.FuncAnimation(Pw, animate,frames = None, fargs= None, interval = 10)
	
plt.show()

File.close()
