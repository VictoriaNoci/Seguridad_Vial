# -*- coding: utf-8 -*-

import math
from IoU_3D import get_3d_box, box3d_iou

def actualizar_metricas3D(lista_GT, lista_BB, IoU, metricas):
    #############################################################################################
    #ACTUALIZACIÓN ESTADÍSTICAS: tp (true positives), fp (false positives) y fn (false negatives)
    if len(lista_BB) == 0:
        for gt in lista_GT:
            metricas[gt[8]][2]+=1 #fn
    
    elif len(lista_GT) > len(lista_BB):
        #fn+=len(lista_GT)-len(lista_BB)
        lista_GT_aux=[]
        for cada_BB in lista_BB:
            distancia=[]
            for cada_GT in lista_GT:
                x=math.pow(cada_GT[1]-cada_BB[1],2)
                y=math.pow(cada_GT[2]-cada_BB[2],2)
                z=y=math.pow(cada_GT[3]-cada_BB[3],2)
                distancia.append(math.sqrt(x+y+z))
            min_index=distancia.index(min(distancia))
            lista_GT_aux.append(lista_GT[min_index])
        
        total=[]
        for lista in (lista_GT,lista_GT_aux):
            for item in lista:
                if item not in total and not (item in lista_GT and item in lista_GT_aux):
                    total.append(item)
        for item_t in total:
            metricas[item_t[8]][2]+=1 #fn
            
        lista_GT=lista_GT_aux

        
    #ORDENAR LAS LISTAS    
    lista_GT_aux=[]
    for cada_BB in lista_BB:
        resta=[]
        for cada_GT in lista_GT:
            resta.append(abs(cada_GT[2]-cada_BB[2]))
        min_index=resta.index(min(resta))
        lista_GT_aux.append(lista_GT[min_index])
    lista_GT=lista_GT_aux
        
    if len(lista_GT) == len(lista_BB):
        for (cada_GT,cada_BB) in zip(lista_GT,lista_BB):
            corners_3d_ground  = get_3d_box((cada_GT[4], cada_GT[5], cada_GT[6]), cada_GT[7], (cada_GT[1], cada_GT[2], cada_GT[3]))
            corners_3d_predict = get_3d_box((cada_BB[4], cada_BB[5], cada_BB[6]), cada_BB[7], (cada_BB[1], cada_BB[2], cada_BB[3]))
            (IOU_3d,IOU_2d)=box3d_iou(corners_3d_predict,corners_3d_ground)
                
            if IOU_3d and IOU_2d > IoU:
                metricas[cada_GT[8]][0]+=1 #tp
            else:
                metricas[cada_GT[8]][1]+=1 #fp
    
    return metricas
    #############################################################################################