#!/usr/bin/python
#-*- coding_ utf8 -*-

from pylab import *
import numpy as np
import scipy
import scipy.ndimage as nd
import matplotlib.pyplot as plt
from collections import Counter

Periodos=[]
longitudes=[0.468,0.59,0.66,0.785,0.83]
Puntos=[[256,1206],[1501,2631],[3016,4246],[4701,5931],[6396,7756]]



""" Funcion que barre sobre las imagenes y calcula:
	- Los centros de masa
	- La transformada de Fourier
	- El periodo
"""

def Pendulo(NoImagMin,NoImagMax,Cuerda):
	tempo=5
	NoImagenes=(NoImagMax-NoImagMin)/float(tempo) +1
	Tutto=np.zeros(NoImagenes+1)
	for k in range(NoImagMin,NoImagMax+1,tempo):
		if k<1000:
			Bola1=imread("./scene00"+str(k)+".png")
		else:
			Bola1=imread("./scene0"+str(k)+".png")
		Ce=np.array((0.9,0.5,0.45))
		S=Bola1-Ce
		D=np.sqrt((S**2).sum(axis=2))
		Gris=Bola1[:,:,0].astype("float")
		min=Gris.min()
		max=Gris.max()
		GrisBin=np.where(D<0.2,1,0)
		Filtro=nd.median_filter(GrisBin,(7,7))
		FiltroNumber,n=nd.label(Filtro)
		#~ print '\n',k
		Elementos=np.zeros(n+1)
		for i in range(0,480):
			counts=np.bincount(FiltroNumber[i])
			longitud=len(counts)
			for j in range(1,longitud):
				a=counts[j]
				Elementos[j]=a+Elementos[j]
		max=np.max(Elementos)
		for l in range(1,n+1):
			if Elementos[l]==max:
				b=l
		MassCenter=nd.measurements.center_of_mass(Filtro,FiltroNumber,b)
		Tutto[(k-NoImagMin)/tempo]=MassCenter[1]
	x=np.arange(0,NoImagenes*tempo +1,tempo)
	FFT=abs(np.fft.fft(Tutto))**2
	Lo=len(Tutto)
	#~ FFT2=FFT[Lo/2:Lo]
	FFT2=FFT[1:Lo]
	MaxFFT2=np.max(FFT2)

	Lol=0
	for q in range(0,len(FFT2)):
		#~ print q,FFT[q]
		if FFT[q]==MaxFFT2:
			#~ Lol=q*tempo
			Lol=q
	PERIODO=NoImagenes/float(Lol*tempo)
	return PERIODO

""" Se calcula los periodos para todas las longitudes """

for i in range(0,len(longitudes),1):
	NoImagMin=Puntos[i][0]
	NoImagMax=Puntos[i][1]
	Cuerda=longitudes[i]
	Periodos.append(Pendulo(NoImagMin,NoImagMax,Cuerda)**2)

""" Se realiza el metodo de minimos cuadrados """
A = np.vstack([longitudes, ones(len(longitudes))]).T
m, c = np.linalg.lstsq(A, Periodos)[0]
g = 4*(pi**2)/m
print 'La constante g en m/s tiene un valor de:',g,'m/s'

Error=abs((g-9.8)/9.8)*100
print 'La constante medida tiene un porcentaje de error de:',Error
