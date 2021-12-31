# -*- coding: utf-8 -*-
from actualizar_metricas2D import actualizar_metricas2D

IoU=0.6
etiquetado=0
detectado=0
n_frames=400

#Métricas
metricas=[[0,0,0],    #EASY   [tp fp fn]
          [0,0,0],    #MEDIUM [tp fp fn]
          [0,0,0]]    #HARD   [tp fp fn]


for i in range(n_frames):
    
    #RECOLECCIÓN DE DATOS
    array_dataset=[]
    fichero='%06d.txt' %i
        
    f=open('../training/label_2/'+fichero,'r')  #BOUNDING BOXES DATASET
    for x in f:
        a=x.split(' ')
        if a[0] != 'DontCare' and a[0] != 'Misc' and int(a[2]) != 3:
            array_dataset.append([a[0], float(a[4]), float(a[6]), float(a[5]), float(a[7]), int(a[2])])
            etiquetado+=1
    f.close()
    
    array_yolo=[]
    f=open('../Resultados-YOLO2D/' + fichero,'r')  #BOUNDING BOXES YOLO (2D)
    a=0
    for x in f:
        a=x.split(' ')
        array_yolo.append([a[0], float(a[1]), float(a[2]), float(a[3]), float(a[4])])
        detectado+=1
    f.close()

    #############################################################################################
    #ACTUALIZACIÓN ESTADÍSTICAS: tp (true positives), fp (false positives) y fn (false negatives)
    metricas=actualizar_metricas2D(array_dataset, array_yolo, IoU, metricas)
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
    #print('tp: ' + str(metricas[i][0]))
    #print('fp: ' + str(metricas[i][1]))
    #print('fn: ' + str(metricas[i][2]))
    print('Precision: ' + str(metricas[i][0]/(metricas[i][0]+metricas[i][1])))
    print('Recall: ' + str(metricas[i][0]/(metricas[i][0]+metricas[i][2])))
    print('--------------------------')

