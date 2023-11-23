import math
import numpy as np

'''
def makearray(minval,maxval,num):  # not needed as linspace does the same thing
    a = [0.0]*num

    for i in range(num):
        a[i] = minval + i*(maxval-minval)/(num-1)

    # note that a[0] is minval and a[num-1] is maxval. 
    # To include both and have num terms, the difference between them needs to be (max-min)/(num-1)

    return a
'''
########################################################################################################################################

def getscalers(Rearth, Mearth, Gconst, Tday, h):
    # h is the Horbit scaler value
    # this function gets the single variable values for one Horbit[i]
    r = Rearth + h   # effective orbital radius
    Vorbit = math.sqrt((Gconst*Mearth)/r)
    Hangle = math.acos(Rearth/r)
    Thorizon = (2*Hangle)/( (Vorbit/r) + (2*math.pi/Tday))
    deltaT = Thorizon/202

    return Vorbit, Hangle, Thorizon, deltaT

########################################################################################################################################

def getWalpha(Hangle, Rearth, h, deltaT):
    # this function returns Wcraft[] and alpha[] for a given height
    # then we can get the max of those in the main function
    r = Rearth + h   # effective orbital radius
    theta = np.linspace(math.pi/2 - Hangle, math.pi/2, 102)
    elevationAng = [0.0]*102
    elevationAng[101] = math.pi/2
    ratio = 0.0
    for i in range(101):  
        # i goes from 0 to 100. i=0 is ok for the calculation
        ratio = (r*math.sin(theta[i])-Rearth)/(r*math.cos(theta[i]))
        elevationAng[i] = math.atan(ratio)

    Wcraft = [0.0]*101
    alpha = [0.0]*100
    Wcraft[0] = (elevationAng[1]-elevationAng[0])/deltaT
    for j in range(100): # go from 0 to 99
        Wcraft[j+1] = (elevationAng[j+2]-elevationAng[j+1])/deltaT
        # Wcraft[1] to [100]
        alpha[j] = (Wcraft[j+1]-Wcraft[j])/deltaT
        # alpha[0] to [99]
    
    return Wcraft, alpha, theta, elevationAng

########################################################################################################################################

def get_TP(Wmax, maxAlpha, moi):
    torque = [[0.0]*11]*11
    Pcraft = [[0.0]*11]*11
    tdat = open("torque values (mNm).txt", 'w')  # open fresh
    pdat = open("Angular Momentum (g cm2 rad ps).txt", 'w')  # open fresh
    for i in range(11):
        torque[i] = [0.0]*11
        Pcraft[i] = [0.0]*11   # Declare again to ensure actual values are saved
        for j in range(11):
            torque[i][j] = round( 1000*maxAlpha[i]*moi[j] ,3)   # torque in mNm
            #print("torque[" + str(i) + "][" + str(j) + "]: " + str(torque[i][j]))
            tdat.write(str(torque[i][j]) + '\t')

            Pcraft[i][j] = round( math.pow(10,7)*Wmax[i]*moi[j] )   # angular momentum in gcm^2 radians/s
            #print("Pcraft[" + str(i) + "][" + str(j) + "]: " + str(Pcraft[i][j]))
            pdat.write(str(Pcraft[i][j]) + '\t')

        tdat.write('\n')
        pdat.write('\n')
    
    tdat.close()
    pdat.close()
    
    return torque, Pcraft

########################################################################################################################################

def calcMinMax(array):   # to get minimum and maximum values for an 11x11 2D array
    minval = min(array[10])
    maxval = max(array[0])
    temp1 = 0
    temp2 = 0
    for i in range(11):
        temp1 = min(array[i])
        temp2 = max(array[i])
        if (temp1 < minval):
            minval = temp1
        if (temp2 > maxval):
            maxval = temp2
    
    return minval, maxval

########################################################################################################################################