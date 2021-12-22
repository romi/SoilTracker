from Phidget22.Phidget import *
from Phidget22.Devices.VoltageRatioInput import *
import numpy as np 
import time 


#samples 
Samples = 10000
Objects = 10
#arrays : all samples are in a single row
Voltage = np.zeros([Objects,Samples])
Weight = np.zeros(Objects)
VoltageMean = np.zeros(Objects)
StandarDeviation = np.zeros(Objects)

#Message
print("Prepare "+str(Objects)+" objects to weight. If possible make them different.\n")

#Object
Input0 = VoltageRatioInput()
#Waits for it to be attached to port  
Input0.openWaitForAttachment(1000)
	

#weight list
for i in range(Objects) :
	w = input("Put a weight on the scale and enter it in grammes\n")
	Weight[i] = int(w)
	for k in range(Samples) :		
		v = Input0.getVoltageRatio()
		#Array of samples 
		Voltage[i,k] = v
		time.sleep(0.01)
		print("weigth %d, mesure %d : %.8f" % (int(w), k, v))
	
	StandarDeviation[i] = np.std(Voltage[i,:],axis = None)
	
	#mean value 
	mean = sum(Voltage[i])/ Samples
	VoltageMean[i] = mean

#indices of sorted Weight array
ind = Weight.argsort()
Weight = Weight[ind]
#sort Voltage array to match Weight array. Rows index is modified
Voltage = Voltage.take(ind,0)
VoltageMean = VoltageMean[ind]
#All data are saved in text files
np.savetxt("Weight.txt",Weight,newline='\n')
np.savetxt("VoltageMean.txt",VoltageMean,newline='\n')
np.savetxt("Standard_Deviation.txt",StandarDeviation,newline='\n')
np.savetxt("Samples.txt",Voltage)
