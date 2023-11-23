import numpy as np
import matplotlib.pyplot as plt
#from mpl_toolkits.mplot3d import Axes3D

import reader
import calculator
import writer

Rearth, Mearth, Gconst, Tday = reader.read_phyinps()

'''
# check if exponents worked fine
print("The physical properties as read are: ")
print("Rearth (m): ",Rearth)
print("Mearth (kg): ",Mearth)
print("Gconst (SI): ",Gconst)
print("Tday (s): ",Tday)
'''

# make arrays for heights and mois in SI units
# Horbit = calculator.makearray(400000,600000,11)  # in m to make 500k as the center as we need
# moi = calculator.makearray(1.5,6.5,11)          # in kgm^2 to make 4 as the center as we need
Horbit = np.linspace(400000,600000,11)
moi = np.linspace(1.5,6.5,11)

print("Horbit: ", Horbit)
print("moi: ", moi)

Wmax = [0.0]*11
Wmaxinarr = [0.0]*11
maxAlpha = [0.0]*11

sname = "Scalers for h in km.txt"
outdat = open(sname,'w')  # open outdat in write mode to refresh it
outdat.write("h(km) \t Vorbit(km/s) \t Hangle(deg) \t Thorizon(min) \t deltaT(s) \n")
outdat.close()

for i in range(11):
    h = Horbit[i]
    Vorbit, Hangle, Thorizon, deltaT = calculator.getscalers(Rearth, Mearth, Gconst, Tday, h)
    Wcraft, alpha, theta, elevationAng = calculator.getWalpha(Hangle, Rearth, h, deltaT)
    writer.write_scalers(sname, h, Vorbit, Hangle, Thorizon, deltaT)
    htemp = round(h/1000)
    name = "vectors for h " + str(htemp) + ".txt"
    # print(name)
    writer.write_vectors(name, Wcraft, alpha, theta, elevationAng, deltaT)
    Wmaxinarr[i] = round( max(Wcraft) ,5)
    Wmax[i] = round( (2*Hangle*(Rearth+h))/(Thorizon*h) ,5)
    maxAlpha[i] = round( max(alpha) ,6)

print("Wmax in array: ", Wmaxinarr)
print("Wmax: ", Wmax)
print("maxAlpha: ", maxAlpha)

name = "WA Values.txt"
writer.write_WA(name, Horbit, Wmax, maxAlpha)

T, P = calculator.get_TP(Wmax,maxAlpha,moi)

'''
for i in range(11):
    for j in range(11):
        print("T[" + str(i) + "][" + str(j) + "]: " + str(T[i][j]))
        print("P[" + str(i) + "][" + str(j) + "]: " + str(P[i][j]))
''' 
# value of T and P is not needed as read_tp() reads it again anyway

torque, Pcraft = reader.read_tp()

writer.write_minmaxTP(torque,Pcraft)

# make 3D plot with torque and pcraft

Horbit = np.linspace(400,600,11)   # new Horbit in km to make graph easier to read
print("New Horbit: ", Horbit)

M, H = np.meshgrid(moi, Horbit)

# Convert z variables to a 2D numpy array. Use reshape() to make them work well with the plotter
torque = np.array(torque).reshape((11, 11))
Pcraft = np.array(Pcraft).reshape((11, 11))

# Create a 3D plot for Torque
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(M, H, torque, cmap="viridis")
ax.set_xlabel("MOI (kgm^2)")
ax.set_ylabel("Horbit (km)")
ax.set_zlabel("Torque (mNm)")
plt.show()

# Create a 3D plot for angular momentum of the craft
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(M, H, Pcraft, cmap="viridis")
ax.set_xlabel("MOI (kgm^2)")
ax.set_ylabel("Horbit (km)")
ax.set_zlabel("Angular Momentum (gcm^2 rad/s)")
plt.show()

