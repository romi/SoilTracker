

from Phidget22.Phidget import *
from Phidget22.Devices.VoltageRatioInput import *
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

objects = 9
samples = 20
offset = 26.1 #N à vide
weight = np.array([])
weight_20 = np.array([])
weight_5_1 = np.array([])
weight_5_2 = np.array([])

Measures = np.zeros([samples,objects]) #array that contains the array
Average_mesures = np.zeros(objects)
o = 1
s = 1

#Creat the four Phidget objects 
Input0 = VoltageRatioInput()
Input1 = VoltageRatioInput()
Input2 = VoltageRatioInput()

#Precise the channel attached to
Input0.setChannel(0)
Input1.setChannel(1)
Input2.setChannel(3)

#Reads the port
Input0.openWaitForAttachment(1500)
Input1.openWaitForAttachment(1500)
Input2.openWaitForAttachment(1500)


#Converts Voltage Ratio to weight
def convertVoltage(voltage0,voltage1,voltage2) :
	
	global weight_20
	global weight_5_1
	global weight_5_2
	
	#Slope and intercept values cellule 51
	#celulle de 5kg (1)
	slope1 = 5767101.655903426
	intercept1 = -456.3077783036904
	
	#Slope and intercept values cellule 52
	slope2 = 6194455.19811738
	intercept2 = -204.67628016617346
	
	#Slope and intercept values cellule 20
    #cellue de 25kg
	slope3 = abs(-25468414.26472861)
	intercept3 = 118.6727476709375

	#Writes the weights mesured and saves them

	weight_v = ((slope2*voltage0+ intercept2)+ (slope1*voltage1+ intercept1) + (slope3*voltage2 + intercept3))*(10**-2) - offset
	weight_20 = np.append(weight_20,(slope3*voltage2 + intercept3)*(10**-2)-offset)
	weight_5_1 = np.append(weight_5_1,(slope2*voltage0 + intercept2)*(10**-2)-offset)
	weight_5_2 = np.append(weight_5_2,(slope1*voltage1 + intercept1)*(10**-2)-offset)
	return weight_v

while(o <= objects) :
	
	print("Put the weight number "+str(o)+" to scale\n")
	w = float(input("Write its value in grammes\n"))
	weight = np.append(weight,w*(10**-2)) #saved in newtoon
	
	while (s <= samples):
		#reads the voltage Ratio
		voltageRatio0 = Input0.getVoltageRatio()
		voltageRatio1 = Input1.getVoltageRatio()
		voltageRatio2 = Input2.getVoltageRatio()
		
		m = convertVoltage(voltageRatio0,voltageRatio1,voltageRatio2)
		Measures[s-1,o-1] = m
		print("weigth %d, mesure %d" % (w*(10**-2), m))
		s += 1
	
	o += 1 
	s = 1



#we calculate the average
for j in range(objects) :
	for i in range(samples) :
		Average_mesures[j] += Measures[i,j]
	
Average_mesures = Average_mesures/samples

#we plot

fig, axs = plt.subplots(4) 

axs[0].plot(weight, "--",label="real weight values")
axs[0].plot(Average_mesures,"y",label="measured weight values")

axs[1].plot(weight_20,"b",label="values measured by 20")

axs[2].plot(weight_5_1,"m",label="values measured by 5_1")
axs[3].plot(weight_5_2,"r",label="values measured by 5_2")

for i in range(4):
	axs[i].legend()

plt.show()


#conclusion erreur de +3 N environ pour les deux directions
