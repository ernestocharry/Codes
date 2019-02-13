#!/usr/bin/python
# -*- coding_ utf8 -*-

from pylab import *
import numpy as np
import scipy
import scipy.ndimage as nd
import matplotlib.pyplot as plt
from scipy.fftpack import fft, fftfreq

from collections import Counter

NoImagMin = 6401
NoImagMax = 7776
tempo = 5
L = 83 #Longitud pendulo
#00236-01256    01516-02761   03016-04381   04711-06151     06401-07776
#               59              66          78,5            83 (mas o mens 0,1)cm
NoImagenes = (NoImagMax-NoImagMin)/tempo;
#Numero de imagenes que se tomara. Img max - imag min / numro de timpo enete cada imagen

Tutto=np.zeros(NoImagenes+1)
TuttoAngulos = np.zeros(NoImagenes+1)

for k in range(NoImagMin,NoImagMax + 1,tempo):
    Bola1 = imread("./scene0" + str(k) +".png")
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

    FiltroNumber,n = nd.label(Filtro)
    print'\n ', k

    
    Elementos  = np.zeros(n+1)
    
    for i in range(0,480): #Debido al número de pixeles de las imágenes
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
           # for i in range (1,n+1):
        #CentroMasa = nd.measurements.center_of_mass(Filtro,FiltroNumber,i)
#print'\n ', i,') Centro de masa:', CentroMasa
    
    MassCenter = nd.measurements.center_of_mass(Filtro,FiltroNumber,b)

#    print'\n\nEl valor que tiene mas elementos de cento de masa es', max,'a este valor le corresponde las coordenadas',MassCenter
# imshow(FiltroNumber)
#   show()
    print MassCenter

    if k==NoImagMin:
        TuttoAngulos[0] = 0
        Xant = MassCenter[0]
        Yant = MassCenter[1]
        ThetaAnterior = 0; 

    if k != NoImagMin:
        print Xant, Yant
        c = sqrt( (Xant - MassCenter[0])**2 + (Yant - MassCenter[1])**2) 
        print c
        
        print 'el cociente es', c/L
        Theta = math.acos(1- (c**2)/(2*(L**2))) # Siempre es positivo
        
        if MassCenter[0] < Xant:
            Theta = -Theta

        Theta = Theta + ThetaAnterior
        TuttoAngulos[(k-NoImagMin)/tempo]=Theta
        ThetaAnterior = Theta
#print Tutto
        Xant = MassCenter[0]
        Yant = MassCenter[1]

x=np.arange(0,NoImagenes*tempo +1,tempo)#Tiempo en segundos

plt.plot(x,TuttoAngulos)

plt.figure()



#FFT = (np.fft.fft(Tutto))/(len(Tutto))
#frq = fftfreq(len(Tutto), tempo)

#plt.vlines(frq, 0, FFT.imag)
#plt.show()


#plt.plot(x,FFT)

FFT = np.fft.fft(TuttoAngulos)
FFT[0:ceil(len(FFT)*0.05)] = 0; #Eliminamos el 5Porciento de os primeros values

plt.plot(abs(FFT))
plt.show()

MaxFFT = np.max(abs(FFT))

a =ceil(len(FFT)*0.05)
b = ceil(len(FFT)*0.5)

print a
print b
Lol2=1

for i in range(int(a),int(b)):
    if (abs(FFT[i])==MaxFFT):
        Lol2=i*tempo

Lo = len(Tutto)
FFT2=FFT[Lo/2:Lo]
#plt.plot(FFT2)

MaxFFT2 = np.max(abs(FFT2))

Lol=0



print'\nEl periodo encontrado es', Lol2

plt.show()
