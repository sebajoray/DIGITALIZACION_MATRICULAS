# -*- coding: utf-8 -*-
"""
Created on Fri Jun 25 23:25:59 2021


"""


# importing cv2 
import cv2
  
# importing numpy 
import numpy as np
from matplotlib import pyplot as plt  
  

#Retorna una imagen solo con lineas horizontales y verticales
# Parametros:
#   - una imagen blanco y negro
#   - cantidad de pixeles para considerar posibles rupturas entre lineas
# Retorna:
#   - Imagen con lineas horizontales y verticales
def GetGridFromImage(image, maxLineGap):
    
    # Kernel para erosionar (y luego dilatar) de altura de un caracter. 
    kernel = np.ones((maxLineGap,1), np.uint8)
      
    # aplica kernel dejando uniones de pixeles con longitud mayor a la de un caracter
    # esto deja lineas horizontales si la imagen esta alineada a los margenes
    imageV = cv2.erode(imageBin, kernel) 
    imageV = cv2.dilate(imageV, kernel, iterations=2)
    
    #aplica kernel transpuesto, solo deja lineas horizontales
    imageH = cv2.erode(imageBin, kernel.T)
    imageH = cv2.dilate(imageH, kernel.T, iterations=2)
     
    
    # combina las lineas horizontales y verticales. Intenta dejar solo la grilla 
    imageOut = cv2.bitwise_or(imageV, imageH)
   
    
    return imageOut


#Retorna una imagen solo con lineas horizontales y verticales
# Parametros:
#   - una imagen blanco y negro con lineas verticales y horizontales
#   - el largo minimo que debe tener una linea  horizontal para ser considerada
#   - el largo minimo que debe tener una linea  verticla para ser considerada
#   - un tamaño (en pixeles) para considerar cuando una linea cortada es continua
#   - el alto promedio de un caracter
# Retorna:
#   - Tupla con lineas horizontales y verticales
def GetLinesFromImage(image, minLineWidth, minLineHeight ,maxLineGap, charAvgHeight):
    (imgH, imgW) = image.shape

    minLineLength = min(minLineWidth, minLineHeight)
    lines = cv2.HoughLinesP(image, rho=1, theta=np.pi / 2, threshold=150, minLineLength=minLineLength, maxLineGap=maxLineGap)

    lh = list()
    lv = list()
    if lines is not None:
        for i in range(0, len(lines)):
            # separa las lineas en horizontales y verticales
            (x1,y1, x2,y2) = lines[i][0]
            lx = abs(x2-x1)
            ly = abs(y2-y1)
            if (lx > ly):
                if lx > minLineWidth: # verifica que cumplan con un minimo largo
                    # no agrega lineas sobre bordes horizontales a distancia de un caracter
                    if y1 > charAvgHeight and y2 < imgH-charAvgHeight:
                        # agrega coordenadas de la linea con su longitud
                        lh.append([x1, y1, x2, y2, lx])
            else:
                if ly > minLineHeight: # verifica que cumplan con un minimo largo
                    # no agrega lineas sobre bordes horizontales a distancia de un caracter
                    # las coordenadas x estan invertidas!
                    if x2 > charAvgHeight and x1 < imgW-charAvgHeight:
                        # agrega coordenadas de la linea con su longitud
                        lv.append([x2, y2, x1, y1, ly])

        # ordena las lineas horizontales de arriba hacia abajo
        lh.sort(key=lambda line: line[1]) # ordena por cordenada y1 (arriba a abajo)
        lv.sort(key=lambda line: line[0]) # ordena por cordenada x1 (derecha a izquierda)
        
        #filtra lineas duplicadas (son consecutivas a nivel pixel pero son conceptualmente la misma)
        listH = [ [0, lh[0][1], imgW, lh[0][1], imgW] ]
        for i in range(1, len(lh)):
            (antLn, actLn) = (listH[-1], lh[i])
            if actLn[1]-antLn[1] < charAvgHeight: # menos distancia que 1 caracter de alto?
                listH[-1] = [0,actLn[1], imgW ,actLn[3], imgW]
            else:
                listH.append([0,actLn[1], imgW ,actLn[3], imgW])
                
        #filtra lineas duplicadas (son consecutivas a nivel pixel pero son conceptualmente la misma)
        listV = [lv[0]]
        for i in range(1, len(lv)):
            (antLn, actLn) = (listV[-1], lv[i])
            if actLn[0]-antLn[0] < charAvgHeight: # menos distancia que 1 caracter de alto?
                listV[-1] = [actLn[0], min(antLn[1], actLn[1]),actLn[2],max(antLn[3], actLn[3]),actLn[3]]
                listV[-1].append( listV[-1][3]-listV[-1][1] )
            else:
                listV.append(actLn)
                    
                
    return (listH, listV)

 

# path 
#path = r'1-1-1-1836-.tif'
path = r'C:\Users\User\proyectos\digitalizacion_matriculas\imagenes\1836 (015)\1-1-1-1836-.jpeg'

 

# Reading an image in default mode 
image = cv2.imread(path) 
 
(imgH, imgW, _) = image.shape

# calcula algunos valores en funcion del tamaño de la image
minLineWidth  = int(imgW*0.50) # 50% del ancho
minLineHeight = int(imgW*0.30) # 35% del alto
maxLineGap    = int(imgW*0.08) # 10% del ancho
charAvgHeight = 32 #alto promedio de un caracter

imageGray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

# convierte la imagen en blanco y negro  y luego invierte para poder aplicar
# operaciones morfologicas como erosion. Queda fondo negro y lineas blancas
(T, imageBin) = cv2.threshold(imageGray, 128, 255, cv2.THRESH_BINARY_INV)

# obtiene lineas horizontales y verticales (puede haber basura)
imageBinGrid = GetGridFromImage(imageBin, maxLineGap)

# recupera lineas de referencia (mas largas) que sirven para caracterizar la planilla
(linesH, linesV) = GetLinesFromImage(imageBinGrid, minLineWidth, minLineHeight, maxLineGap, charAvgHeight)

for l in linesH:
    cv2.line(image, (l[0], l[1]), (l[2], l[3]), (0,0,255), 3, cv2.LINE_AA)  
    print("LH: (%d,%d)->(%d)" %  (l[0], l[1], l[4]) )

for l in linesV:
    cv2.line(image, (l[0], l[1]), (l[2], l[3]), (0,255,0), 3, cv2.LINE_AA)  
    print("LV: (%d,%d)->(%d)" %  (l[0], l[1], l[4]) )


# invierte la imagen para obtener el fondo blanco y lineas negras
imageOut = 255-image
# Displaying the image 
#cv2.imshow(window_name, image) 
plt.imshow(image)
cv2.imwrite(path+'-BigLinesGrid.png', imageBinGrid)
cv2.imwrite(path+'-BigLines.png', image)




