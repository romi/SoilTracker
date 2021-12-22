from matplotlib import pyplot as plt
from scipy import stats
import numpy as np

#samples 
Samples = 10000
Objects = 10
#arrays 
Weight = np.zeros(Objects) 
VoltageMean = np.zeros(Objects)
StandarDeviation = np.zeros(Objects)
WmeanStd = np.zeros(Objects)
WmeanA= np.zeros([Objects,Samples])
Voltage = np.zeros([Objects,Samples])
#counter
j = 0
#extraction of data from text saved files to numpy arrays
fil = open("Text_files/Standard_Deviation.txt","r")
File = open("Text_files/VoltageMean.txt","r")
fichier = open("Text_files/Samples.txt","r")
f = open("Text_files/Weight.txt","r")

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
	

#Linear regression : a linear approximation of the graphs -- useful data : slope & intercept

slope, intercept, r_value, p_value, std_err = stats.linregress(VoltageMean,Weight)
#We write the slope and intercept in a text file
fSlope = open("LinearRegression.txt","w")
fSlope.write(str(slope)+"\n")
fSlope.write(str(intercept)+"\n")
fSlope.close()

#We plot the relation between voltage and weight, and the linear approximation of this graph
#equation : slope*Vmean + intercept = weight 
plt.plot(VoltageMean, slope*VoltageMean + intercept, label = 'W ='+ str(slope)+'*V+'+ str(intercept))
plt.legend()


#Standard deviation in grammes 
WmeanA = slope*Voltage + intercept 

for i in range(Objects) : 
	WmeanStd[i] = np.std(WmeanA[i,:],axis = None)

#ploting weight = f(Voltage mean)

plt.grid()
plt.errorbar(VoltageMean, Weight,yerr = WmeanStd,fmt = "o--")
plt.xlabel("Voltage")
plt.ylabel("Weight")
plt.title("Weight = f(Voltage)")
#We save the plotted figure
plt.savefig("Weight_=_f(Voltage_Mean).png");

plt.figure(2)

#standard deviation 
plt.grid()
plt.plot(Weight,WmeanStd,"o--")
plt.xlabel("Weight (grammes)")
plt.ylabel("Standard deviation (grammes)")
plt.title("σ  = f(Weight)")

#We save the plotted figure
plt.savefig("Standard_Deviation.png");

plt.show()
