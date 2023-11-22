import csv

def read_phyinps():
    inpdat = open("physical inputs.txt",'r')

    line = inpdat.readline() # truncate the first row
    line = inpdat.readline() # get the line
    row = line.split(":")      # get row as an array
    Rearth = float(row[0])    
    line = inpdat.readline() # get the next line
    row = line.split(":")     
    Mearth = float(row[0])    
    line = inpdat.readline() # get the next line
    row = line.split(":")     
    Gconst = float(row[0])    
    line = inpdat.readline() # get the next line
    row = line.split(":")     
    Tday = float(row[0])   
    inpdat.close()     # close the file after done reading

    return Rearth, Mearth, Gconst, Tday

########################################################################################################################################

def read_tp():
    torque = [[0.0]*11]*11
    Pcraft = [[0.0]*11]*11
    tdat = open("torque values (mNm).txt",'r')
    pdat = open("Angular Momentum (g cm2 rad ps).txt",'r')
    for i in range(11):
        tline = tdat.readline() # get the line
        pline = pdat.readline() # get the line
        trow = tline.split("\t")      # get row as an array
        prow = pline.split("\t")      # get row as an array
        torque[i] = [0.0]*11
        Pcraft[i] = [0.0]*11        # declare again in loop to ensure new values each time

        for j in range(11):
            torque[i][j] = float(trow[j])
            Pcraft[i][j] = float(prow[j])
    
    return torque, Pcraft

########################################################################################################################################

