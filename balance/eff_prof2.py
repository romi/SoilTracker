from numpy import *
import matplotlib.pyplot as plt 


# Sans rotation de la binette
effort1 = fromfile('v_sans_tourné_raw.txt', 'float32', sep='\n')
profondeur1 = fromfile('posZ_noDig_filtered.txt', 'float32', sep='\n')
courantz1 = fromfile('currentZAxis_noDig_filtered.txt', 'float32', sep='\n')
courantb1 = fromfile('currentWAxis_noDig_filtered.txt', 'float32', sep='\n')
ny1 = 0
nx1 = 0
ny2 = 0
nx2 = 0
ny3 = 0
nx3 = 0
"""
with open('v_sans_tourné_raw.txt') as infp:
	for line in infp:
		if line.strip():
			ny1+=1

with open('posZ_noDig_filtered.txt') as infp:
	for line in infp:
		if line.strip():
			nx1+=1

	a1 = int(nx1/ny1)

	print ('Valeur de a1= %d' %a1) 

x1 = effort1[::1]
y1 = profondeur1[::a1]

with open('currentZAxis_noDig_filtered.txt') as infp:
	for line in infp:
		if line.strip():
			ny2+=1

	a2 = int(nx1/ny2)

	print ('Valeur de a2= %d' %a2)

x2 = courantz1[::1]
y2 = profondeur1[::a2]

with open('currentWAxis_noDig_filtered.txt') as infp:
	for line in infp:
		if line.strip():
			ny3+=1

	a3 = int(nx1/ny3)

	print ('Valeur de a3= %d' %a3)

x3 = courantb1[::1]
y3 = profondeur1[::a3]

figure1, ax1 = plt.subplots(2, 2) 
  
ax1[0, 0].plot(y1[:-1],x1 ) 
ax1[0, 0].set_xlabel('Profondeur')
ax1[0, 0].set_ylabel('Efforts')
ax1[0, 0].set_title('Courbe des efforts verticaux en fonction de la profondeur sans rotation')
  
ax1[0, 1].plot(y2[:],x2 ) 
ax1[0, 1].set_xlabel('Profondeur')
ax1[0, 1].set_ylabel('Courant Z')
ax1[0, 1].set_title('Courbe du courant Z en fonction de la profondeur sans rotation')
  
ax1[1, 0].plot(y3[:],x3 ) 
ax1[1, 0].set_xlabel('Profondeur')
ax1[1, 0].set_ylabel('Courant W')
ax1[1, 0].set_title('Courbe des courant W en fonction de la profondeur sans rotation')

plt.show()
"""
#Avec rotation de la binette 
effort2 = fromfile('v_tourné_raw.txt', 'float32', sep='\n')
profondeur2 = fromfile('posZ_dig_filtered.txt', 'float32', sep='\n')
courantz2 = fromfile('currentZAxis_dig_filtered.txt', 'float32', sep='\n')
courantb2 = fromfile('currentWAxis_dig_filtered.txt', 'float32', sep='\n')
ny4 = 0
nx4 = 0
ny5 = 0
nx5 = 0
ny6 = 0
nx6 = 0

with open('v_tourné_raw.txt') as infp:
	for line in infp:
		if line.strip():
			ny4+=1

with open('posZ_dig_filtered.txt') as infp:
	for line in infp:
		if line.strip():
			nx4+=1

	a4 = int(nx4/ny4)

	print ('Valeur de a4= %d' %a4) 

x4 = effort2[::1]
y4 = profondeur2[::a4]

with open('currentZAxis_dig_filtered.txt') as infp:
	for line in infp:
		if line.strip():
			ny5+=1

	a5 = int(nx4/ny5)

	print ('Valeur de a5= %d' %a5)

x5 = courantz1[::1]
y5 = profondeur1[::a5]

with open('currentWAxis_dig_filtered.txt') as infp:
	for line in infp:
		if line.strip():
			ny6+=1

	a6 = int(nx4/ny6)

	print ('Valeur de a6= %d' %a6)

x6 = courantb1[::1]
y6 = profondeur1[::a6]

figure2, ax2 = plt.subplots(2, 2) 
  
ax2[0, 0].plot(y4[:-3],x4 ) 
ax2[0, 0].set_xlabel('Profondeur')
ax2[0, 0].set_ylabel('Efforts')
ax2[0, 0].set_title('Courbe des efforts verticaux en fonction de la profondeur avec rotation')
  
ax2[0, 1].plot(y5[:],x5 ) 
ax2[0, 1].set_xlabel('Profondeur')
ax2[0, 1].set_ylabel('Courant Z')
ax2[0, 1].set_title('Courbe du courant Z en fonction de la profondeur avec rotation')
  
ax2[1, 0].plot(y6[:],x6 ) 
ax2[1, 0].set_xlabel('Profondeur')
ax2[1, 0].set_ylabel('Courant W')
ax2[1, 0].set_title('Courbe des courants W en fonction de la profondeur avec rotation')
  

plt.show()
