

for j in range(266,267,5):
    Bola1 = imread("./scene00" + str(j) +".png")
#scene00 256/401/291/296/301/306


    Gris = Bola1[:,:,0].astype("float")


    #    Gris[0:210, 360:390]=0
    #Gris[330:350,360:380]=0
    #Gris[190:216,250:270]=0
    #Gris[330:355,218:250]=0

    min = Gris.min()
    max = Gris.max()

    GrisBin = where(Gris<1, 0,225)

    Filtro = nd.median_filter(GrisBin, (7,7))

#imshow(Filtro, cmap="gray")
    #show()

    FiltroNumber,n = nd.label(Filtro)

    
    Elementos  = np.zeros(n+1)
    
    for i in range(0,480):
        counts = np.bincount(FiltroNumber[i])
        longitud = len(counts)
        print counts
        
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
    print'\n--------------------------\n', j
    for i in range (1,n+1):
        CentroMasa = nd.measurements.center_of_mass(Filtro,FiltroNumber,i)
        print'\n ', i,') Centro de masa:', CentroMasa
    
    MassCenter = nd.measurements.center_of_mass(Filtro,FiltroNumber,b)

    print'El valor que tiene mas elementos de cento de masa es', max,'a este valor le corresponde las coordenadas',MassCenter
    imshow(FiltroNumber)
    show()

