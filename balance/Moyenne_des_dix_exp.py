import numpy as np 
from matplotlib import pyplot as plt

num_data_per_exp = np.loadtxt("Text_files/data_of_exp.txt")
max_data = int(np.max(num_data_per_exp))
PATH = "Text_files/Experiments/Trapèze/data_modifiées/"
current_freq = 10**-3 #seconds
effort_freq = 10**-1 #seconds
inter = 0

current_data_binette_i = np.zeros([max_data,10])
current_data_x_i = np.zeros([max_data,10])
current_data_z_i = np.zeros([max_data,10])
f_v_i = np.zeros([max_data,10])
f_h_i = np.zeros([max_data,10])

current_data_binette_mean = np.zeros(max_data)
current_data_x_mean = np.zeros(max_data)
current_data_z_mean = np.zeros(max_data)
f_v_mean = np.zeros(max_data)
f_h_mean = np.zeros(max_data)


def interpolation(x1,y1,x2,y2,x) :
	
	return y1+(x-x1)*((y2-y1)/(x2-x1))

#Mise des données à la même taille
for i in range(10) :
	
		#load modified files 
		current_time = np.loadtxt(PATH+"Exp"+str(i+1)+"_current_time.txt")
		current_data_binette = np.loadtxt(PATH+"Exp"+str(i+1)+"_current_data_binette.txt")
		current_data_x = np.loadtxt(PATH+"Exp"+str(i+1)+"_current_data_x.txt")
		current_data_z = np.loadtxt(PATH+"Exp"+str(i+1)+"_current_data_z.txt")
		f_v = np.loadtxt(PATH+"Exp"+str(i+1)+"_fv.txt")
		f_h = np.loadtxt(PATH+"Exp"+str(i+1)+"_fh.txt")
		f_time = np.loadtxt(PATH+"Exp"+str(i+1)+"_ftime.txt")
		
		#Fill time files with the correponded frequency
		for n in range(np.size(current_time)-1,max_data-1) :
			current_time = np.append(current_time,current_time[n] + current_freq)
		
		for n in range(np.size(f_time)-1,max_data-1) :
			f_time = np.append(f_time,f_time[n] + effort_freq)
			
		#interpolation of data 
		length = int(num_data_per_exp[i])
		diff = max_data - length
		step = np.ceil(length/(length - diff)) #the step of data at which we interpolate
		
	
		for v in range(1,length-1) :
			if(inter == max_data -1):
				break
			if(v%step == 0):
				current_data_x_i[inter][i] = interpolation(current_time[v-1],current_data_x[v-1],current_time[v+1],current_data_x[v+1],current_time[v])
				current_data_z_i[inter][i] = interpolation(current_time[v-1],current_data_z[v-1],current_time[v+1],current_data_z[v+1],current_time[v])
				current_data_binette_i[inter][i] = interpolation(current_time[v-1],current_data_binette[v-1],current_time[v+1],current_data_binette[v+1],current_time[v])
				f_v_i[inter][i] = interpolation(f_time[v-1],f_v[v-1],f_time[v+1],f_v[v+1],f_time[v])
				f_h_i[inter][i] = interpolation(f_time[v-1],f_h[v-1],f_time[v+1],f_h[v+1],f_time[v])
				inter +=1
			else :
				current_data_x_i[inter][i] = current_data_x[v]
				current_data_binette_i[inter][i] = current_data_binette[v]
				current_data_z_i[inter][i] = current_data_z[v]
				f_v_i[inter][i] = f_v[v]
				f_h_i[inter][i] = f_h[v]
				inter += 1
		np.size(current_data_x_i[:0]) 

			
#Moyenne des experiences
for i in range(10) :
	
	current_data_binette_mean = np.add(current_data_binette_mean,current_data_binette_i[:i])
	current_data_x_mean = np.add(current_data_x_mean,current_data_x_i[:i])
	current_data_z_mean = np.add(current_data_z_mean,current_data_z_i[:i])
	f_v_mean = np.add(f_v_mean,f_v_i[:i])
	f_h_mean = np.add(f_h_mean,f_h[:i])
	
current_data_binette_mean /= 10
current_data_x_mean /= 10
current_data_z_mean /= 10
f_v_mean /= 10
f_h_mean /= 10

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
ax[0][0].plot(f_time,f_h_mean,"m",label="Horizontal efforts")
ax[0][0].legend()
ax[0][1].plot(current_time,current_data_x_mean,"b",label="Courant axe x")
ax[0][1].legend()
ax[1][0].set_ylim(0.0,MasseMaxh)
ax[1][0].plot(f_time,f_h_mean,"m",label="Horizontal effort")
ax[1][0].legend()
ax[1][1].plot(current_time,current_data_binette_mean,"y",label="Courant binette")
ax[1][1].legend()
#fig1.savefig("Graph/Experiments/Trapèze/"+Radical+"H_CX_Cb.png")

al[0][0].set_ylim(0.0,MasseMaxv)
al[0][0].plot(f_time,f_v_mean,"g",label="Vertical effort")
al[0][0].legend()
al[0][1].plot(current_time,current_data_z_mean,color="orange",label="Courant axe z")
al[0][1].legend()
al[1][0].set_ylim(0.0,MasseMaxv)
al[1][0].plot(f_time,f_v_mean,"g",label="Vertical effort")
al[1][0].legend()
al[1][1].plot(current_time,current_data_binette_mean,"y",label="Courant binette")
al[1][1].legend()
#fig2.savefig("Graph/Experiments/Trapèze/"+Radical+"V_CZ_Cb.png")
	
ar[0][0].set_ylim(0.0,MasseMaxv)
ar[0][0].scatter(current_data_z_mean,f_v_mean, label="f(courant_z) = effort_vertical")
ar[0][0].legend()
ar[0][1].set_ylim(0.0,MasseMaxv)
ar[0][1].scatter(current_data_binette_mean,f_v_mean,label="f(courant_binette) = effort_vertical")
ar[0][1].legend()
ar[1][0].set_ylim(0.0,MasseMaxh)
ar[1][0].scatter(current_data_x_mean,f_h_mean,label="f(courant_x) = effort_horizontal")
ar[1][0].legend()
ar[1][1].set_ylim(0.0,MasseMaxh)
ar[1][1].scatter(current_data_binette_mean,f_h_mean,label="f(courant_binette) = effort_horizontal")
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
	
			
	
		
