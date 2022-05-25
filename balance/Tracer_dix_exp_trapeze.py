import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

#Font 
SMALL_SIZE = 16
MEDIUM_SIZE = 20
BIGGER_SIZE = 32

diff = np.loadtxt("Text_files/Experiments/Trapèze/Différence_aquisition.txt")
PATH = "Text_files/Experiments/Trapèze"
data = []

for i in range(0,10):
	
	#Utilisation des données voisines (4 voisins)

	Radical = "/Exp"+str(i+1)+"/"
	it = "Iteration0"+str(i+1)+"/"
	#Array of data
	f_h = np.loadtxt(PATH+Radical+"h1raw.txt")
	f_v = np.loadtxt(PATH+Radical+"v1raw.txt")
	f_time = np.loadtxt(PATH+Radical+"h1time.txt")
	current_time = np.loadtxt("Current_data/Trapèze/"+it+"currentXAxis_time.txt")
	current_data_binette = np.loadtxt("Current_data/Trapèze/"+it+"currentWAxis_filtered.txt")
	current_data_x = np.loadtxt("Current_data/Trapèze/"+it+"currentXAxis_filtered.txt")
	current_data_z = np.loadtxt("Current_data/Trapèze/"+it+"currentZAxis_filtered.txt")
	
	#difference of acquisition between current and effort
	difference = diff[i] #en secondes
	MasseMaxv = 180
	MasseMaxh = 40

	offset_v = 126
	offset_h = 4.3

	#obtenir une synchronisation - commencer en même de temps que wilou
	value = f_time[0]
	counter = 1
	#Valeurs de courants en absolue
	current_data_x = abs(current_data_x)
	current_data_z = abs(current_data_z)

	while(value < difference):
		counter += 1
		value = f_time[counter]

	f_h = f_h[counter:]
	f_v = f_v[counter:]
	f_time = f_time[counter:]
	#Wilson : 6000 données
	#Razane : ~150 données
	#Une donnée tout les 20
	counter = 0
	j = 0
	l = 1
	while(1):
		try:
			
			if(counter == 20*j):
				current_data_binette[j] = (current_data_binette[counter] + current_data_binette[counter-2] + current_data_binette[counter-1] + current_data_binette[counter+1] + current_data_binette[counter+2])/4
				current_data_x[j] = (current_data_x[counter] + current_data_x[counter-2] +current_data_x[counter-1] + current_data_x[counter+1] + current_data_x[counter+2])/4
				current_data_z[j] = (current_data_z[counter] + current_data_z[counter-2] + current_data_z[counter-1] + current_data_z[counter+1] + current_data_z[counter+2])/4
				current_time[j] = current_time[counter]
				l += 1
			
				j += 1
			counter += 1
		
		except : 
			break
			
	print(l)
	#Mettre les arrays des courants et efforts à la même taille 
	if l < j : 
		current_time = current_time[:l-1]
		current_data_binette = current_data_binette[:l-1]
		current_data_x = current_data_x[:l-1]
		current_data_z = current_data_z[:l-1]
		f_v = f_v[:l-1]
		f_h = f_h[:l-1]
		f_time = f_time[:l-1]
		np.savetxt(PATH+"/data_modifiées/Exp"+str(i+1)+"_current_time.txt",current_time)
		np.savetxt(PATH+"/data_modifiées/Exp"+str(i+1)+"_current_data_binette.txt",current_data_binette)
		np.savetxt(PATH+"/data_modifiées/Exp"+str(i+1)+"_current_data_x.txt",current_data_x)
		np.savetxt(PATH+"/data_modifiées/Exp"+str(i+1)+"_current_data_z.txt",current_data_z)
		np.savetxt(PATH+"/data_modifiées/Exp"+str(i+1)+"_fv.txt",f_v)
		np.savetxt(PATH+"/data_modifiées/Exp"+str(i+1)+"_fh.txt",f_h)
		np.savetxt(PATH+"/data_modifiées/Exp"+str(i+1)+"_ftime.txt",f_time)
		data.append(l)
	else:
		j = np.size(f_h)
		current_data_binette = current_data_binette[:j]
		current_data_x = current_data_x[:j]
		current_data_z = current_data_z[:j]
		current_time = current_time[:j]
		np.savetxt(PATH+"/data_modifiées/Exp"+str(i+1)+"_current_time.txt",current_time)
		np.savetxt(PATH+"/data_modifiées/Exp"+str(i+1)+"_current_data_binette.txt",current_data_binette)
		np.savetxt(PATH+"/data_modifiées/Exp"+str(i+1)+"_current_data_x.txt",current_data_x)
		np.savetxt(PATH+"/data_modifiées/Exp"+str(i+1)+"_current_data_z.txt",current_data_z)
		np.savetxt(PATH+"/data_modifiées/Exp"+str(i+1)+"_fv.txt",f_v)
		np.savetxt(PATH+"/data_modifiées/Exp"+str(i+1)+"_fh.txt",f_h)
		np.savetxt(PATH+"/data_modifiées/Exp"+str(i+1)+"_ftime.txt",f_time)
		data.append(j)
	

	plt.rc('font',size=SMALL_SIZE)
	plt.rc('axes',titlesize=SMALL_SIZE)
	plt.rc('axes',labelsize=MEDIUM_SIZE)
	plt.rc('xtick',labelsize=SMALL_SIZE)
	plt.rc('ytick',labelsize=SMALL_SIZE)
	plt.rc('legend',fontsize=SMALL_SIZE)
	plt.rc('figure',titlesize=BIGGER_SIZE)
	
	#Tracer :
	#efforts horizontal fct de axe x et binette 
	#efforts vertical fct de axe z et binette

	#efforts horizontaux
	fig1,ax = plt.subplots(2,2)
	#efforts verticaux
	fig2,al = plt.subplots(2,2)
	#relation courant effort
	fig3, ar = plt.subplots(2,2)


	ax[0][0].set_ylim(0.0,MasseMaxh)
	ax[0][0].plot(f_time,f_h,"m",label="Horizontal efforts",linewidth=3)
	ax[0][0].legend()
	ax[0][1].plot(current_time,current_data_x,"b",label="Courant axe x",linewidth=3)
	ax[0][1].legend()
	ax[1][0].set_ylim(0.0,MasseMaxh)
	ax[1][0].plot(f_time,f_h,"m",label="Horizontal effort",linewidth=3)
	ax[1][0].legend()
	ax[1][1].plot(current_time,current_data_binette,"r",label="Courant binette",linewidth=3)
	ax[1][1].legend()
	#fig1.savefig("Graph/Experiments/Trapèze/"+Radical+"H_CX_Cb.png")

	al[0][0].set_ylim(0.0,MasseMaxv)
	al[0][0].plot(f_time,f_v,"g",label="Vertical effort",linewidth=3)
	al[0][0].legend()
	al[0][1].plot(current_time,current_data_z,color="orange",label="Courant axe z",linewidth=3)
	al[0][1].legend()
	al[1][0].set_ylim(0.0,MasseMaxv)
	al[1][0].plot(f_time,f_v,"g",label="Vertical effort",linewidth=3)
	al[1][0].legend()
	al[1][1].plot(current_time,current_data_binette,"r",label="Courant binette",linewidth=3)
	al[1][1].legend()
	#fig2.savefig("Graph/Experiments/Trapèze/"+Radical+"V_CZ_Cb.png")
		
	ar[0][0].set_ylim(0.0,MasseMaxv)
	ar[0][0].scatter(current_data_z,f_v, label="f(courant_z) = effort_vertical",linewidth=3)
	ar[0][0].legend()
	ar[0][1].set_ylim(0.0,MasseMaxv)
	ar[0][1].scatter(current_data_binette,f_v,label="f(courant_binette) = effort_vertical",linewidth=3)
	ar[0][1].legend()
	ar[1][0].set_ylim(0.0,MasseMaxh)
	ar[1][0].scatter(current_data_x,f_h,label="f(courant_x) = effort_horizontal",linewidth=3)
	ar[1][0].legend()
	ar[1][1].set_ylim(0.0,MasseMaxh)
	ar[1][1].scatter(current_data_binette,f_h,label="f(courant_binette) = effort_horizontal",linewidth=3)
	ar[1][1].legend()
	#fig3.savefig("Graph/Experiments/Trapèze/"+Radical+"Efforts_fct_courant.png")
	for i in range(0,2):
		al[i][0].set_ylabel("effort en N")
		ax[i][0].set_ylabel("effort en N")
		al[i][1].set_ylabel("courant en A")
		ax[i][1].set_ylabel("courant en A")
		for j in range(0,2) :
			ax[i][j].set_xlabel("temps en s")
			al[i][j].set_xlabel("temps en s")
			ar[i][j].set_ylabel("effort en N")
			ar[i][j].set_xlabel("courant en A")

	plt.show()

"""		
	print("size ="+str(np.size(current_time)))
	
	#Superposition des dix graphes de efforts horizontaux en fonction du courant binette
	#Ca ne ressemble à rien
	plt.xlabel("Courant binette en A")
	plt.ylabel("Effort horizontal en N")
	plt.title("Superposition des dix expériences") 
	plt.plot(current_data_binette,f_h)
	
	if(i == 9):
		plt.show()
	
"""
