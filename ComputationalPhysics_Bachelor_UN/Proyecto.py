#!/usr/bin/python
# -*- coding_ utf8 -*-

from pylab import *
import numpy as np
import scipy
import scipy.ndimage as nd
import matplotlib.pyplot as plt
import math
from scipy.fftpack import fft, fftfreq
from collections import Counter
from numpy import polyval, polyfit


#tempo = 5
#NoImagMin = 6401
#NoImagMax = 7776
#LongPendulo = 83

OmegCuadrados=[]

# What kind of L?
L = [46.8, 59, 66, 78.5, 83]
InversoLongitudes = [100./46.8, 100./59, 100./66, 100./78.5, 100./83]

# Fotogramas que funcionan
Puntos = [[236,1256],[1516,2761],[3016,4381],[4711,6151],[6401,7776]]

#00236-01256    01516-02761   03016-04381   04711-06151     06401-07776
#      46.8         59              66          78,5            83 (mas o mens 0,1)cm

#Numero de imagenes que se tomara. Img max - imag min / numro de timpo enete cada imagen


def Pendulo(NoImagMin,NoImagMax):
    tempo = 5
    NoImagenes = (NoImagMax-NoImagMin)/tempo;
    Tutto=np.zeros(NoImagenes+1)
    for k in range(NoImagMin,NoImagMax + 1,tempo):
        if k<1000:
            Bola1=imread("./scene00"+str(k)+".png")
        else:
            Bola1=imread("./scene0"+str(k)+".png")
        Ce = np.array((0.9, 0.5, 0.45))
        S= Bola1-Ce
        D = np.sqrt((S**2).sum(axis=2))
        Gris = Bola1[:,:,0].astype("float")
        GrisBin= np.where(D<0.2,1,0)
        Filtro = nd.median_filter(GrisBin, (7,7))
        FiltroNumber,n = nd.label(Filtro)
        # Center of mass
        Elementos  = np.zeros(n+1)

        for i in range(0,480):
            counts = np.bincount( list(map(float, FiltroNumber[i])))
            longitud = len(counts)
            for j in range(1,longitud):
                a = counts[j]
                Elementos[j] = a + Elementos[j]
        max = np.max(Elementos)
        for l in range(1,n+1):
            if Elementos[l]==max:
                b = l
        MassCenter = nd.measurements.center_of_mass(Filtro,FiltroNumber,b)
        Tutto[(k-NoImagMin)/tempo]=MassCenter[1]
    FFT = np.fft.fft(Tutto)
    L0 = len(FFT)
    b=ceil(L0*0.5)

    FFT[0]=0
    FFT[b:L0] = 0

    FFT = abs(FFT)
    MaxFFT = np.max(FFT)

    Lol2=np.argmax(FFT)
    OmegaCuad = float((Lol2*tempo*tempo*10/(NoImagMax-NoImagMin))**2)
    return OmegaCuad


for i in range(0,len(InversoLongitudes),1):
    print '\nEl programa se encuentra corriendo sobre las '
    print 'imagenes correspondientes a la longitud de ',
    print L[i], 'cm'
    NoImagMin=Puntos[i][0]
    NoImagMax=Puntos[i][1]
    Pendulo(NoImagMin,NoImagMax)
    OmegCuadrados.append(Pendulo(NoImagMin,NoImagMax))

coeficientes = polyfit(InversoLongitudes,OmegCuadrados,1)
g= np.pi*np.pi*4*coeficientes[0]
gporcentual = abs((g-980)*100/980);

print 'El valor de la gravedad encontrado es', g, ' en cm/s^2. '
print 'El error porcentual de este valor es ', gporcentual
