import calculator
import math

def write_scalers(name, h, Vorbit, Hangle, Thorizon, deltaT):
    outdat = open(name,'a')  # open outdat in append
    h = round(h/1000,2)  # h in km
    Vorbit = round(Vorbit/1000,2)  # Vorbit in km/s
    Hangle = round( (180*Hangle)/math.pi, 2)  # Hangle in degrees
    Thorizon = round(Thorizon/60, 2)    # Thorizon in min
    deltaT = round(deltaT, 2)      # deltaT in 2 decimal places
    outdat.write(str(h) + '\t' + str(Vorbit) + '\t' + str(Hangle) + '\t' + str(Thorizon) + '\t' + str(deltaT) + '\n')

    outdat.close()

########################################################################################################################################

def write_vectors(name, Wcraft, alpha, theta, elevationAng, deltaT):   # only for 1 h value
    outdat = open(name, 'w')  # open fresh for 1 h
    outdat.write("theta (deg) \t time (s) \t elevationAng (deg) \t Wcraft (deg/s) \t alpha (deg/s^2)\n")
    time = 0.0
    ang = round( (theta[0]*180)/math.pi, 1)
    elv = round( (elevationAng[0]*180)/math.pi, 3)
    outdat.write(str(ang) + "\t" + str(time) + "\t" + str(elv) + '\n')   # only angle for first time step
    time = round(time + deltaT,2)
    ang = round( (theta[1]*180)/math.pi, 1)    
    elv = round( (elevationAng[1]*180)/math.pi, 3)
    w = round( (Wcraft[0]*180)/math.pi, 4)
    outdat.write(str(ang) + "\t" + str(time) + "\t" + str(elv) + "\t" + str(w) + '\n')   # angle n w for 2nd time step

    for i in range(100):
        time = round(time + deltaT,2)
        ang = round( (theta[i+2]*180)/math.pi, 1)    
        elv = round( (elevationAng[i+2]*180)/math.pi, 3)
        w = round( (Wcraft[i+1]*180)/math.pi, 5)
        acc = round( (alpha[i]*180)/math.pi, 6)
        outdat.write(str(ang) + "\t" + str(time) + "\t" + str(elv) + "\t" + str(w) + "\t" + str(acc) + '\n')
        # write all from 0 to 99 for acceleration

    outdat.close()

########################################################################################################################################

def write_WA(name, Horbit, Wmax, maxAlpha):
    outdat = open(name, 'w')  # open fresh
    outdat.write("Height(km) \t Wmax(rad/s) \t maxAlpha(rad/s^2) \t Wmax(deg/s) \t maxAlpha(deg/s^2) \n")

    for i in range(11):
        h = round(Horbit[i]/1000)
        w = round( Wmax[i], 5)    
        a = round( maxAlpha[i], 6)
        wd = round( (Wmax[i]*180)/math.pi, 5)    
        ad = round( (maxAlpha[i]*180)/math.pi, 6)
        outdat.write(str(h) + "\t\t" + str(w) + "\t\t" + str(a) + "\t\t" + str(wd) + "\t\t" + str(ad) + '\n')

    outdat.close()

########################################################################################################################################

def write_minmaxTP(torque, Pcraft):
    
    mintorque,maxtorque = calculator.calcMinMax(torque)
    minpcraft,maxpcraft = calculator.calcMinMax(Pcraft)
    '''
    mintorque = t1
    maxtorque = t2
    minpcraft = p1
    maxpcraft = p2
    '''

    print("Min Torque (mNm): " + str(mintorque) + "Max Torque (mNm): " + str(maxtorque))
    print("Min Angular Momentum (gcm^2 rad/s): " + str(minpcraft) + "Max Angular Momentum (gcm^2 rad/s): " + str(maxpcraft))

    outdat = open("Min Max TP.txt", 'w')
    outdat.write(str(mintorque) + " \t: Minimum torque (mNm)\n")
    outdat.write(str(maxtorque) + " \t: Maximum torque (mNm)\n")
    outdat.write(str(minpcraft) + " \t: Minimum Angular Momentum (gcm^2 rad/s)\n")
    outdat.write(str(maxpcraft) + " \t: Maximum Angular Momentum (gcm^2 rad/s)\n")

    outdat.close()

########################################################################################################################################