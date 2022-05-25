from Phidget22.Phidget import *
from Phidget22.Devices.VoltageRatioInput import *

from matplotlib import pyplot as plt
from matplotlib import animation
from matplotlib.pyplot import figure
import time 
from datetime import datetime 

import numpy as np

class DataContainer:
    def __init__(self):
        self.raw = []
        self.t = []
        self.start = 0.0
        self.first_measure = True
        return None
        
    def measure(self,data):
        if(self.first_measure):
            self.t_start = time.time()
            self.first_measure = False
        self.raw.append(data)
        self.t.append(time.time()-self.t_start)
        return None
        
    def save(self, prefix):
        np.savetxt(prefix+"raw.txt",self.raw)
        np.savetxt(prefix+"time.txt",self.t)
        return None
      
       

t = 0 #time in seconds
MasseMax = 35 #kg
Max_N_Data = 30 #Data to display before "moving the window"
Interval = 25 #ms
counter = 0 
g = 10 #gravity constant


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

#Slope and intercept values cellule 780

slope4 = 722779.3974552653
intercept4 = -21.2563001758013

#Set up the figure, axis 
Pv = plt.figure(figsize=(10,10)) #figure to be display
x = []
y = [] #vertical effort
y2 = [] #horizontal effort
#labels
plt.grid()
plt.xlabel("Time(s)")
plt.ylabel("Weight(N)")
plt.title("Force mesures")
#limit for y axis = 35 kg
plt.ylim(0.0, MasseMax*g)
#data to show
lines = [plt.plot([],[])[0] for _ in range(2)]
legend = plt.legend()

#initilisation of 2D object
def init() :
	global legend 
	for line in lines :
		line.set_data([],[])
	
	legend.remove()
	legend = plt.legend()
	
	return lines + [legend]

#initialisation of arrays that contains saved data
h = DataContainer()
v = DataContainer()
	
#Creat the four Phidget objects 
Input0 = VoltageRatioInput()
Input1 = VoltageRatioInput()
Input2 = VoltageRatioInput()
Input3 = VoltageRatioInput()
#Precise the channel attached to
Input0.setChannel(0)
Input1.setChannel(1)
Input2.setChannel(3)
Input3.setChannel(2)

#WAiting the ports to connect - 4 seconds max
Input0.openWaitForAttachment(4000)
Input1.openWaitForAttachment(4000)
Input2.openWaitForAttachment(4000)
Input3.openWaitForAttachment(4000)
Input3.openWaitForAttachment(4000)

SAVE_PATH = "Text_files/Experiments/EnfctProfondeur/"

#saving data at the end of visualisation (event handling)	
def on_press(event) :
	
	global v
	global h
	
	if event :
		v.save(SAVE_PATH+"v_tourné_")
		h.save(SAVE_PATH+"h_tourné_")
		#delets objects
		Input0.close()
		Input1.close()
		Input2.close()
		Input3.close()
	

	
#animated figure	
def animate(i,v,h) :
	
	global t
	global legend 
	global Input0
	global Input1
	global Input2
	global Input3
	global counter 
	global slop1
	global slop2
	global slop3
	global slop4
	global intercept1
	global intercept3
	global intercept2
	global intercept4
	
	
	start = time.time()
	if  t== 0:
		print("start acquisition at : "+str(start))
	
	#reads the voltage Ratio
	voltage0 = Input0.getVoltageRatio()
	voltage1 = Input1.getVoltageRatio()
	voltage2 = Input2.getVoltageRatio()
	voltage3 = Input3.getVoltageRatio()
	
	
	weight_v = ((slope2*voltage0+ intercept2)+ (slope1*voltage1+ intercept1) + (slope3*voltage2 + intercept3))*(10**-2)
	v.measure(weight_v)
	
	weight_h = (slope4*voltage3 + intercept4)*(10**-2)
	h.measure(weight_h)
	
	#fill the axis arrays
	x.append(t)
	y.append(weight_v)
	y2.append(weight_h)
	
	#time
	t += round((time.time()+1)-time.time())
	#moving the window each Max_N_data samples
	if len(x) > Max_N_Data :
		x.pop(0)
		y.pop(0)
		y2.pop(0)
	
	#array of drawing 
	lines[0].set_data([x,y])
	lines[0].set_label("Vertical efforts")
	lines[1].set_data([x,y2])
	lines[1].set_label("Horizontal efforts")
	
	#refreshing the window + legend
	Pv.gca().relim()
	Pv.gca().autoscale_view(tight = True)
	legend.remove()
	legend = plt.legend()
	
	
	return lines + [legend]

#animate
anim = animation.FuncAnimation(Pv, animate, init_func = init,frames = None, fargs= (v,h), interval = Interval)
#waiting for closing window event
Pv.canvas.mpl_connect('close_event',on_press) #closing the window

plt.show()



