# -*- coding: utf-8 -*-
from actualizar_metricas3D import actualizar_metricas3D
from actualizar_metricas2D import area

IoU=0.6
umbral_score=0.8
etiquetado=0
detectado=0
n_frames=400

#Métricas
metricas=[[0,0,0],    #EASY   [tp fp fn]
          [0,0,0],    #MEDIUM [tp fp fn]
          [0,0,0]]    #HARD   [tp fp fn]

for i in range(n_frames):
    
    #RECOLECCIÓN DE DATOS
    fichero='%06d.txt' % i
    
    array_lidar=[]
    f=open('../LiDAR/Resultados_conv_bien_score/' + fichero,'r')  #BOUNDING BOXES LiDAR (2D)
    a=0
    for x in f:
        a=x.split(' ')
        array_lidar.append([a[0], float(a[4]), float(a[6]), float(a[5]), float(a[7]), float(a[15])])
    f.close()
    
    array_yolo=[]
    f=open('../Resultados-YOLO2D/' + fichero,'r')  #BOUNDING BOXES YOLO (2D)
    a=0
    for x in f:
        a=x.split(' ')
        array_yolo.append([a[0], float(a[1]), float(a[2]), float(a[3]), float(a[4]), float(a[5])/100])
    f.close()
    
    lista_GT=[]
    lista_BB=[]
    f=open('../LiDAR/Resultados/' + fichero, 'r')  #DETECCION LiDAR (3D)
    for x in f:
        campos=x.split(' ')
        if campos[0] == 'GT':
            if campos[3].split(',')[0] != 'DontCare' and campos[3].split(',')[0] != 'Misc' and int(campos[19].split('\n')[0]) != 3:
                lista_GT.append([campos[3].split(',')[0],float(campos[5].split(',')[0]), float(campos[7].split(',')[0]), float(campos[9].split(',')[0]), float(campos[11].split(',')[0]), float(campos[13].split(',')[0]), float(campos[15].split(',')[0]), float(campos[17].split(',')[0]), int(campos[19].split('\n')[0])])
        elif campos[0] == 'BB':
            lista_BB.append([campos[3].split(',')[0],float(campos[5].split(',')[0]), float(campos[7].split(',')[0]), float(campos[9].split(',')[0]), float(campos[11].split(',')[0]), float(campos[13].split(',')[0]), float(campos[15].split(',')[0]), float(campos[17].split(',')[0])])
    f.close()
    
    #VALIDACIÓN DE LAS DETECCIONES
    #Nos quedamos con las detecciones de LiDAR validadas por YOLO
    #Si YOLO no valida pero score de LiDAR es alta, LiDAR se valida (> 0.8)
    array_detecc=[]
    if array_yolo and array_lidar:
        for (lidar, lidar_BB) in zip(array_lidar,lista_BB):
            flag_coincid=False
            for yolo in array_yolo:
                score_lidar=lidar[5]
                coincidencia=area(yolo[1:5],lidar[1:])
                if coincidencia:
                    flag_coincid=True
                    break
            if flag_coincid or (score_lidar > umbral_score):
                array_detecc.append(lidar_BB)
    
    detectado+=len(array_detecc)
    
    #############################################################################################
    #ACTUALIZACIÓN ESTADÍSTICAS: tp (true positives), fp (false positives) y fn (false negatives)
    metricas=actualizar_metricas3D(lista_GT,array_detecc,IoU,metricas)
    ########################
    
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

