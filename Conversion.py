import numpy as np

n_frames=400

path_resultados='../../Resultados-score/Resultados3D/'
path_resultados2='../../Resultados-score/Resultados2D/'
path_calibration='../../training/calib/'

def read_calibration(file_path: str):
    with open(path_calibration + file_path, "r") as f:
        lines = f.readlines()

        #T_cam_velo (4x4)
        Tr_velo_to_cam = np.array(lines[5].split(": ")[1].split(" "), dtype=np.float32).reshape((3, 4))
        #R_cam (3x3) y t (1x3) -> LiDAR
        R_cam, t = Tr_velo_to_cam[:, :3], Tr_velo_to_cam[:, 3]
        Tr_velo_to_cam = np.vstack([Tr_velo_to_cam , [0,0,0,1]]) #Expandir Tr_velo_to_cam a (4x4)

        #P_i_rect -> P2 por cámara color izq (3x4)
        P_i = np.array(lines[2].split(": ")[1].split(" "), dtype=np.float32).reshape((3, 4))

        #R_0_rect (4x4)
        R_rect = np.array(lines[4].split(": ")[1].split(" "), dtype=np.float32).reshape((3, 3))
        R_rect = np.vstack([R_rect , [0,0,0]]) #Expandir R_rect a (4x4)
        R_rect = np.column_stack([R_rect , [0,0,0,1]]) #Expandir R_rect a (4x4)

        return R_cam, t, P_i, R_rect,Tr_velo_to_cam


for i in range(n_frames):
    fichero='%06d.txt' % i
    f=open(path_resultados + fichero, 'r')
    f1=open(path_resultados2 + fichero, 'w')
    for x in f:
        campos=x.split(' ')
        if campos[0] == 'BB':
            #print(str(campos))

            #CONVERSIÓN YAW [-pi, pi]
            yaw=float(campos[17].split(',')[0])
            rotation_y = -yaw-np.pi/2
            while rotation_y < -np.pi:
                rotation_y += (np.pi * 2)
            while rotation_y > np.pi:
                rotation_y -= (np.pi * 2)

            #CONVERSIÓN CENTROIDE CON R y t
            x=float(campos[5].split(',')[0])
            y=float(campos[7].split(',')[0])
            z=float(campos[9].split(',')[0])

            centroide=np.array([x,y,z])
            R_cam,t,P_i,R_rect,Tr_velo_to_cam=read_calibration(fichero)  #Lectura matrices de calibración
            centroides_conv=np.matmul(R_cam,(centroide+t))

            #Cálculo coordenadas 3D BBox
            l=float(campos[11].split(',')[0])
            h=float(campos[15].split(',')[0])
            w=float(campos[13].split(',')[0])
            x_corners=[l/2, l/2,-l/2,-l/2,l/2,l/2,-l/2,-l/2]
            y_corners=[0,0,0,0,-h,-h,-h,-h]
            z_corners=[w/2,-w/2,-w/2,w/2,w/2,-w/2,-w/2,w/2]

            #Añadir sobre centroide para calculo del 3D BBox
            for i in range(8):
                x_corners[i]+=x
                y_corners[i]+=y
                z_corners[i]+=z

            #Proyeccion de coordenadas 3D en plano imagen
            x_cam=[]
            y_cam=[]
            for j in range(8):
                pto_lidar=np.array([x_corners[j], y_corners[j], z_corners[j], 1])
                A=np.matmul(P_i,R_rect)
                B=np.matmul(A,Tr_velo_to_cam)
                pto_camara=np.matmul(B,pto_lidar) #Sin normalizar
                pto_camara[0]=pto_camara[0]/pto_camara[2]
                pto_camara[1]=pto_camara[1]/pto_camara[2]
                x_cam.append(pto_camara[0])
                y_cam.append(pto_camara[1])

            #Obtención del BBox en 2D
            x_min=min(x_cam)
            x_max=max(x_cam)
            y_min=min(y_cam)
            y_max=max(y_cam)

            #Creación línea y escritura
            linea='%s 0 0 %f %f %f %f %f %f %f %f %f %f %f %f %f\n' % (campos[3].split(',')[0], rotation_y, x_min, y_min, x_max, y_max, h, w, l, centroides_conv[0], centroides_conv[1], centroides_conv[2], rotation_y, float(campos[19].split('\n')[0]))
            #linea2='%s 0 0 0 %f %f %f %f %f %f %f %f %f %f %f\n' % (campos[3].split(',')[0], x_min, y_min, x_max, y_max, h, w, l, centroides_conv[0], centroides_conv[1], centroides_conv[2], rotation_y)
            f1.write(linea)
            #f1.write(linea2)
    f1.close()
    f.close()
            #lista.append([campos[3].split(',')[0],float(campos[5].split(',')[0]), float(campos[7].split(',')[0]), float(campos[9].split(',')[0]), float(campos[11].split(',')[0]), float(campos[13].split(',')[0]), float(campos[15].split(',')[0]), float(campos[17].split('\n')[0])])
