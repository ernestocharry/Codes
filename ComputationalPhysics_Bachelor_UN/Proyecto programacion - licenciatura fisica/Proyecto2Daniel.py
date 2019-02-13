#!/usr/bin/python
# -*- coding_ utf8 -*-

from pylab import *
import numpy as np
import scipy
import scipy.ndimage as nd
import matplotlib.pyplot as plt

from collections import Counter

NoImagMin = 266
NoImagMax = 297
tempo = 5

NoImagenes = (NoImagMax-NoImagMin)/tempo;
#Numero de imagenes que se tomara. Img max - imag min / numro de timpo enete cada imagen


Tutto=np.zeros(NoImagenes+1)

for k in range(266,297,5):
    Bola1 = imread("./scene00" + str(k) +".png")
#scene00 256/401/291/296/301/306
    Ce = np.array((0.9, 0.5, 0.45))
    S= Bola1-Ce
    
    D = np.sqrt((S**2).sum(axis=2))
    
   
    Gris = Bola1[:,:,0].astype("float")


    #    Gris[0:210, 360:390]=0
    #Gris[330:350,360:380]=0
    #Gris[190:216,250:270]=0
    #Gris[330:355,218:250]=0

    min = Gris.min()
    max = Gris.max()

    #GrisBin = where(Gris<1, 0,225)
    GrisBin= np.where(D<0.2,1,0)

    Filtro = nd.median_filter(GrisBin, (7,7))

#imshow(Filtro, cmap="gray")
    #show()

    FiltroNumber,n = nd.label(Filtro)

    
    Elementos  = np.zeros(n+1)
    
    for i in range(0,480):
        counts = np.bincount(FiltroNumber[i])
        longitud = len(counts)
        #   print counts
        
        for j in range(1,longitud):
            a = counts[j]
            Elementos[j] = a + Elementos[j]

    max = np.max(Elementos)

    for l in range(1,n+1):
        if Elementos[l]==max:
            b = l
        
            
#for i in range(0,480):
        #for j in range(0,640):
        #   if ( FiltroNumber[i,j] == 5):
    #       print FiltroNumber[i,j]

    
    #  CentroMasa = nd.measurements.center_of_mass(Filtro,FiltroNumber,3)
    #Debe mandar la matrix binaria, la matriz que resulta de nd.label y n indica el numero que desea calcular el centro de masa, si este numero es n entonces por defecto tomara el mayor. Puede ser de 1, 2...
    print'\n--------------------------\n', k
        # for i in range (1,n+1):
        #CentroMasa = nd.measurements.center_of_mass(Filtro,FiltroNumber,i)
#print'\n ', i,') Centro de masa:', CentroMasa
    
    MassCenter = nd.measurements.center_of_mass(Filtro,FiltroNumber,b)

    print'\n\nEl valor que tiene mas elementos de cento de masa es', max,'a este valor le corresponde las coordenadas',MassCenter
    imshow(FiltroNumber)
    show()

    Tutto[(k-NoImagMin)/tempo]=MassCenter[1]
print Tutto

x=np.array([0,1,2,3,4,5,6])
plt.plot(Tutto)
plt.show()

