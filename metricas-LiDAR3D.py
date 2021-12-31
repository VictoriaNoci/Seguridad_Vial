from actualizar_metricas3D import actualizar_metricas3D

IoU=0.6
n_frames=400
path_resultados='../LiDAR/Resultados/'

#Métricas
metricas=[[0,0,0],    #EASY   [tp fp fn]
          [0,0,0],    #MEDIUM [tp fp fn]
          [0,0,0]]    #HARD   [tp fp fn]


for i in range(n_frames):
    
    #RECOLECCIÓN DE DATOS
    #Datos procedentes detección con PointPillars
    lista_GT=[]  #Etiquetado
    lista_BB=[]  #Detectado
    fichero='%06d.txt' % i
    f=open(path_resultados + fichero, 'r')
    for x in f:
        campos=x.split(' ')
        if campos[0] == 'GT':
            if campos[3].split(',')[0] != 'DontCare' and campos[3].split(',')[0] != 'Misc' and int(campos[19].split('\n')[0]) != 3:
                lista_GT.append([campos[3].split(',')[0],float(campos[5].split(',')[0]), float(campos[7].split(',')[0]), float(campos[9].split(',')[0]), float(campos[11].split(',')[0]), float(campos[13].split(',')[0]), float(campos[15].split(',')[0]), float(campos[17].split(',')[0]), int(campos[19].split('\n')[0])])
        elif campos[0] == 'BB':
            lista_BB.append([campos[3].split(',')[0],float(campos[5].split(',')[0]), float(campos[7].split(',')[0]), float(campos[9].split(',')[0]), float(campos[11].split(',')[0]), float(campos[13].split(',')[0]), float(campos[15].split(',')[0]), float(campos[17].split(',')[0])])
    f.close()
    
    #############################################################################################
    #ACTUALIZACIÓN ESTADÍSTICAS: tp (true positives), fp (false positives) y fn (false negatives)
    metricas=actualizar_metricas3D(lista_GT,lista_BB,IoU,metricas)
    #############################################################################################
       
         
print('---ESTADÍSTICAS TOTALES---')
for i in range(len(metricas)):
    if i==0:
        print('--------------------------')
        print('EASY')
    elif i==1:
        print('MEDIUM')
    elif i==2:
        print('HARD')
    # print('tp: ' + str(metricas[i][0]))
    # print('fp: ' + str(metricas[i][1]))
    # print('fn: ' + str(metricas[i][2]))
    print('Precision: ' + str(metricas[i][0]/(metricas[i][0]+metricas[i][1])))
    print('Recall: ' + str(metricas[i][0]/(metricas[i][0]+metricas[i][2])))
    print('--------------------------')
