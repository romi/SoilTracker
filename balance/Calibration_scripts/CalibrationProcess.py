from matplotlib import pyplot as plt
from scipy import stats
import numpy as np


#Font 
SMALL_SIZE = 16
MEDIUM_SIZE = 20
BIGGER_SIZE = 32
#samples 
Samples = 10000
Objects = 10
#arrays : all samples are in a single row
Weight = np.zeros(Objects) 
VoltageMean = np.zeros(Objects)
StandarDeviation = np.zeros(Objects)
WmeanStd = np.zeros(Objects)
WmeanA= np.zeros([Objects,Samples])
Voltage = np.zeros([Objects,Samples])

j = 0

fil = open("/Text_files/Calibration/Standard_Deviation5_1.txt","r")
File = open("balance/Text_files/Calibration/VoltageMean5_1.txt","r")
fichier = open("balance/Text_files/Calibration/Samples5_1.txt","r")
f = open("balance/Text_files/Calibration/Weight5_1.txt","r")

for i in range(Objects) :
	Weight[i] = float(f.readline().strip())
	StandarDeviation[i] = float(fil.readline().strip())
	VoltageMean[i] = float(File.readline().strip())
	Content = fichier.readline().strip().split()
	
	for s in Content :
		Voltage[i,j] = float(s)
		j +=1
	j = 0
	
		
fil.close()
File.close()
fichier.close()
f.close()


#Linear regression

slope, intercept, r_value, p_value, std_err = stats.linregress(VoltageMean,Weight)
r_slope  = round(slope,2);
r_intercept = round(intercept,2)

fSlope = open("Text_files/Calibration/LinearRegression20.txt","w")
fSlope.write(str(slope)+"\n")
fSlope.write(str(intercept)+"\n")
fSlope.close()

#equation : slope*Vmean + intercept = weight 
plt.plot(VoltageMean, slope*VoltageMean + intercept, label = 'W ='+ str(r_slope)+'*V'+str(r_intercept))
plt.legend()


#Standard deviation in grammes 2
WmeanA = slope*Voltage + intercept 

for i in range(Objects) : 
	WmeanStd[i] = np.std(WmeanA[i,:],axis = None)

#ploting weight = f(Voltage mean)

plt.rc('font',size=SMALL_SIZE)
plt.rc('axes',titlesize=SMALL_SIZE)
plt.rc('axes',labelsize=MEDIUM_SIZE)
plt.rc('xtick',labelsize=SMALL_SIZE)
plt.rc('ytick',labelsize=SMALL_SIZE)
plt.rc('legend',fontsize=SMALL_SIZE)
plt.rc('figure',titlesize=BIGGER_SIZE)

#plt.grid()
plt.errorbar(VoltageMean, Weight,yerr = WmeanStd,fmt = "o--")
plt.xlabel("Voltage")
plt.ylabel("Weight(grammes)")
plt.title("Weight = f(Voltage) - cellule 20")

plt.savefig("Weight_=_f(Voltage_Mean)20.png");

plt.figure(2)

#standard deviation 
plt.grid()
plt.plot(Weight,WmeanStd,"o--")
plt.xlabel("Weight (grammes)")
plt.ylabel("Standard deviation (grammes) - cellule 20")
plt.title("σ  = f(Weight)")

plt.savefig("Standard_Deviation20.png");


#Histogramme de distribution
#plt.figure(figsize=(10,5))
#for i in range(3,6) :
#	plt.hist(Voltage[i,:],bins='auto');
	
#plt.xlabel("Voltage Ratio")
#plt.ylabel("Frequency")
#plt.title("Distribution of mesures : Object 4 to 6")

#plt.savefig("Histogramme de mesure")

plt.show()
