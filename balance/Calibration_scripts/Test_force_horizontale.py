import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

#Font 
SMALL_SIZE = 16
MEDIUM_SIZE = 20
BIGGER_SIZE = 32

f = open("Text_files/Calibration/WeightExperiment_horizontal.txt","r")
t = open("Text_files/Calibration/Test_dynano_force_horizontal.txt","r")
w_e = np.array([])
w_r = np.array([])
w_e_2 = np.array([])
i = 0
j = 1
offset = 5.7 #N

f.readline()
w_e = np.append(w_e,round(float(f.readline().strip('\n')),1))
w_e = np.append(w_e,round(float(f.readline().strip('\n')),1))

while(1) :
	try :
		if j == 0 :
			w_e_2 = np.append(w_e_2,w_e[i]- offset) 
			j = 1
			w_e = np.append(w_e,round(float(f.readline().strip('\n')),1))
			i += 1
		else :
			while w_e[i+1] >= w_e[i]-0.4 and w_e[i+1] <= w_e[i]+0.4 :
				w_e = np.append(w_e,round(float(f.readline().strip('\n')),1))
				i += 1
				print(i)
			j = 0
	except :
		break


while(1) :
	try :
		w_r = np.append(w_r,float(t.readline().strip(" N\n")))
	except :
		break

plt.rc('font',size=SMALL_SIZE)
plt.rc('axes',titlesize=SMALL_SIZE)
plt.rc('axes',labelsize=MEDIUM_SIZE)
plt.rc('xtick',labelsize=SMALL_SIZE)
plt.rc('ytick',labelsize=SMALL_SIZE)
plt.rc('legend',fontsize=SMALL_SIZE)
plt.rc('figure',titlesize=BIGGER_SIZE)

fig,ax = plt.subplots(2)

ax[0].plot(w_r,"--",label="real values")
ax[1].plot(w_e_2,"m",label="measured values")

ax[0].legend()
ax[1].legend()
plt.show()
