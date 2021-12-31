import math

#############################################################################################
def area(a, b):  # returns None if rectangles don't intersect (COMPROBACIÓN IoU)
    # a = [xmin, xmax, ymin, ymax]
    # b = [xmin, xmax, ymin, ymax]
    dx = min(a[1], b[1]) - max(a[0], b[0])
    dy = min(a[3], b[3]) - max(a[2], b[2])
    if (dx >= 0) and (dy >= 0):
        return dx*dy
    else:
        return None
#############################################################################################

#############################################################################################
def actualizar_metricas2D(dataset, yolo, IoU, metricas):
    #Actualizar métricas
    #Objeto anotado y detectado = tp (True positive)
    if dataset and yolo:
        if (len(dataset) != len(yolo)): #Hay que elegir cómo comparar IoU
            if len(dataset) > len(yolo):  #Objeto anotado que no se ha detectado
                #Hay que quitar los que sobran 
                dataset_aux=[]
                
                for a in yolo:
                    distancia=[]
                    media_x_a=(a[2]+a[1])/2
                    media_y_a=(a[4]+a[3])/2
                    for b in dataset:
                        media_x_b=(b[2]+b[1])/2
                        media_y_b=(b[4]+b[3])/2
                        x=math.pow(media_x_b-media_x_a,2)
                        y=math.pow(media_y_b-media_y_a,2)
                        distancia.append(math.sqrt(x+y))
                    min_index=distancia.index(min(distancia))
                    dataset_aux.append(dataset[min_index])
                    
                #fn
                total=[]
                for lista in (dataset,dataset_aux):
                    for item in lista:
                        if item not in total and not (item in dataset and item in dataset_aux):
                            total.append(item)
                for item_t in total:
                    metricas[item_t[5]][2]+=1
                
                dataset=dataset_aux
                
            elif len(yolo) > len(dataset): #Objeto detectado no anotado
                metricas[0][1]+=len(yolo)-len(dataset)
                metricas[1][1]+=len(yolo)-len(dataset)
                metricas[2][1]+=len(yolo)-len(dataset)

                #Hay que quitar los que sobran de person
                yolo_aux=[]
                for a in dataset:
                    distancia=[]
                    media_x_a=(a[2]+a[1])/2
                    media_y_a=(a[4]+a[3])/2
                    for b in yolo:
                        media_x_b=(b[2]+b[1])/2
                        media_y_b=(b[4]+b[3])/2
                        x=math.pow(media_x_b-media_x_a,2)
                        y=math.pow(media_y_b-media_y_a,2)
                        distancia.append(math.sqrt(x+y))
                        
                    min_index=distancia.index(min(distancia))
                    yolo_aux.append(yolo[min_index])
                    
                #fp
                total=[]
                for lista in (yolo,yolo_aux):
                    for item in lista:
                        if item not in total and not (item in yolo and item in yolo_aux):
                            total.append(item)
                for item_t in total:
                    metricas[0][1]+=1
                    
                yolo=yolo_aux
                
        elif len(dataset) > 1:  #Elegir las combinaciones (ordenar)
            #Hay que ordenar
            yolo_aux=[]
            for a in dataset:
                distancia=[]
                media_x_a=(a[2]+a[1])/2
                media_y_a=(a[4]+a[3])/2
                for b in yolo:
                    media_x_b=(b[2]+b[1])/2
                    media_y_b=(b[4]+b[3])/2
                    x=math.pow(media_x_b-media_x_a,2)
                    y=math.pow(media_y_b-media_y_a,2)
                    distancia.append(math.sqrt(x+y))
                min_index=distancia.index(min(distancia))
                yolo_aux.append(yolo[min_index])
            yolo=yolo_aux
        
        #COMPROBACIÓN IoU
        for j in range(len(dataset)):
            area_solapada=area(dataset[j][1:5],yolo[j][1:])
            if area_solapada != None:
                area_dataset=(dataset[j][2]-dataset[j][1])*(dataset[j][4]-dataset[j][3])
                area_yolo=(yolo[j][2]-yolo[j][1])*(yolo[j][4]-yolo[j][3])
                if area_solapada >= IoU*area_dataset and area_solapada >= IoU*area_yolo:
                    if dataset[j][5] != 3:
                        metricas[dataset[j][5]][0]+=1  #tp
                else:
                    if dataset[j][5] != 3:
                        metricas[dataset[j][5]][1]+=1  #fp
         
    #Objeto anotado pero no detectado = fn (False negative)
    elif dataset and not yolo:
        for dataset_lista in dataset:
            if dataset_lista[5] != 3:
                metricas[dataset_lista[5]][2]+=1
                
    #No objeto anotado pero detectado = fp (False positive)
    elif not dataset and yolo:
        metricas[0][1]+=len(yolo)-len(dataset)
        
    return(metricas)
#############################################################################################
