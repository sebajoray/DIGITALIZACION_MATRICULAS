# -*- coding: utf-8 -*-
"""
Created on Fri Jun 25 23:25:59 2021


"""


# importing cv2 
import cv2
  
# importing numpy 
import numpy as np
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

from matplotlib import pyplot as plt  

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (0,0,255)
GREEN = (0,255,0)
BLUE = (255,0,0)

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
path = r'1-1-1-1838-.tif'

 

# Reading an image in default mode 
image = cv2.imread(path) 
 
(imgH, imgW, _) = image.shape

vertice_superior_izquierdo = (0, 0)
vertice_superior_derecho = (imgW, 0)
vertice_inferior_izquierdo = (0, imgH)
vertice_inferior_derecho = (imgW, imgH)

# calcula algunos valores en funcion del tamaño de la image
minLineWidth  = int(imgW*0.50) # 50% del ancho
minLineHeight = int(imgW*0.35) # 35% del alto
maxLineGap    = int(imgW*0.08) # 10% del ancho
charAvgHeight = 32 #alto promedio de un caracter

# image = cv2.line(image, (0,10), (imgW, 10), (0,0,0), 3, cv2.LINE_AA)
# cv2.line(image, (0, imgH), (imgW, imgH), (255,255,255), 3, cv2.LINE_AA)

imageGray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

# convierte la imagen en blanco y negro  y luego invierte para poder aplicar
# operaciones morfologicas como erosion. Queda fondo negro y lineas blancas
(T, imageBin) = cv2.threshold(imageGray, 128, 255, cv2.THRESH_BINARY_INV)

# obtiene lineas horizontales y verticales (puede haber basura)
imageBinGrid = GetGridFromImage(imageBin, maxLineGap)

## Agregar lineas exteriores (cubo exterior)
cv2.line(imageBinGrid, vertice_superior_izquierdo, vertice_superior_derecho, WHITE, 6, cv2.LINE_AA)
cv2.line(imageBinGrid, vertice_inferior_izquierdo, vertice_inferior_derecho, WHITE, 6, cv2.LINE_AA)

cv2.line(imageBinGrid, vertice_superior_izquierdo, vertice_inferior_izquierdo, WHITE, 6, cv2.LINE_AA)
cv2.line(imageBinGrid, vertice_superior_derecho, vertice_inferior_derecho, WHITE, 6, cv2.LINE_AA)

# # recupera lineas de referencia (mas largas) que sirven para caracterizar la planilla
# (linesH, linesV) = GetLinesFromImage(imageBinGrid, minLineWidth, minLineHeight, maxLineGap, charAvgHeight)

# for l in linesH:
#     cv2.line(image, (l[0], l[1]), (l[2], l[3]), RED, 3, cv2.LINE_AA)  
#     # print("LH: (%d,%d)->(%d)" %  (l[0], l[1], l[4]) )
# for l in linesV:
#     cv2.line(image, (l[0], l[1]), (l[2], l[3]), GREEN, 3, cv2.LINE_AA)  
#     # print("LV: (%d,%d)->(%d)" %  (l[0], l[1], l[4]) )

## Agregar lineas exteriores (cubo exterior)
# cv2.line(image, vertice_superior_izquierdo, vertice_superior_derecho, RED , 6, cv2.LINE_AA)
# cv2.line(image, vertice_inferior_izquierdo, vertice_inferior_derecho, RED, 6, cv2.LINE_AA)

# cv2.line(image, vertice_superior_izquierdo, vertice_inferior_izquierdo, GREEN, 6, cv2.LINE_AA)
# cv2.line(image, vertice_superior_derecho, vertice_inferior_derecho, GREEN, 6, cv2.LINE_AA)

# invierte la imagen para obtener el fondo blanco y lineas negras
imageOut = 255-image
# Displaying the image 
cv2.imwrite(path+'-BigLinesGrid.png', imageBinGrid)
# cv2.imwrite(path+'-BigLines.png', image)

###########################################################################
# Detect contours for following box detection
# imageByN = cv2.cvtColor(imageBinGrid, cv2.COLOR_BGR2GRAY)
contours, hierarchy = cv2.findContours(imageBinGrid, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

def sort_contours(cnts, method="left-to-right"):
    # initialize the reverse flag and sort index
    reverse = False
    i = 0
    # handle if we need to sort in reverse
    if method == "right-to-left" or method == "bottom-to-top":
        reverse = True
    # handle if we are sorting against the y-coordinate rather than
    # the x-coordinate of the bounding box
    if method == "top-to-bottom" or method == "bottom-to-top":
        i = 1
    # construct the list of bounding boxes and sort them from top to
    # bottom
    boundingBoxes = [cv2.boundingRect(c) for c in cnts]
    (cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
    key=lambda b:b[1][i], reverse=reverse))
    # return the list of sorted contours and bounding boxes
    return (cnts, boundingBoxes)

# Sort all the contours by top to bottom.
contours, boundingBoxes = sort_contours(contours, method="top-to-bottom")

boundingBoxes = boundingBoxes[1:2]
contours = contours[1:2]
#Creating a list of heights for all detected boxes
heights = [boundingBoxes[i][3] for i in range(len(boundingBoxes))]
#Get mean of heights
mean = np.mean(heights)

#Create list box to store all boxes in  
box = []
# Get position (x,y), width and height for every contour and show the contour on image
for c in contours:
    x, y, w, h = cv2.boundingRect(c)
    if (w<imgW and h<imgH) and (h > charAvgHeight * 2):
        cv2.rectangle(image,(x,y),(x+w,y+h),BLUE,2)
        box.append([x,y,w,h])

cv2.imwrite(path+'-Boxes.png', image)

#Creating two lists to define row and column in which cell is located
row=[]
column=[]
j=0
# Sorting the boxes to their respective row and column
for i in range(len(box)):
    # No tienen titulo las columnas
    # if(i==0):
    #     column.append(box[i])
    #     previous=box[i]
    # else:
    # if(box[i][1]<=previous[1]+mean/2):
    column.append(box[i])
    # previous=box[i]
    # if(i==len(box)-1):
    row.append(column)
    # else:
    # row.append(column)
    # column=[]
    # # previous = box[i]
    # column.append(box[i])

#calculating maximum number of cells
countcol = 0
for i in range(len(row)):
    countcol = len(row[i])
    if countcol > countcol:
        countcol = countcol


#Retrieving the center of each column
center = [int(row[i][j][0]+row[i][j][2]/2) for j in range(len(row[i])) if row[0]]
center=np.array(center)
center.sort()


finalboxes = []
for i in range(len(row)):
    lis=[]
    for k in range(countcol):
        lis.append([])
    for j in range(len(row[i])):
        diff = abs(center-(row[i][j][0]+row[i][j][2]/4))
        minimum = min(diff)
        indexing = list(diff).index(minimum)
        lis[indexing].append(row[i][j])
    finalboxes.append(lis)

#from every single image-based cell/box the strings are extracted via pytesseract and stored in a list
outer=[]
for i in range(len(finalboxes)):
    for j in range(len(finalboxes[i])):
        inner=''
        if(len(finalboxes[i][j])==0):
            outer.append(' ')
        else:
            for k in range(len(finalboxes[i][j])):
                y,x,w,h = finalboxes[i][j][k][0],finalboxes[i][j][k][1], finalboxes[i][j][k][2],finalboxes[i][j][k][3]
                finalimg = imageOut[x:x+h, y:y+w]
                kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 1))
                border = cv2.copyMakeBorder(finalimg,2,2,2,2,   cv2.BORDER_CONSTANT,value=[255,255])
                resizing = cv2.resize(border, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
                dilation = cv2.dilate(resizing, kernel,iterations=1)
                erosion = cv2.erode(dilation, kernel,iterations=1)

                
                out = pytesseract.image_to_string(erosion)
                if(len(out)==0):
                    out = pytesseract.image_to_string(erosion, config='--psm 2')
                inner = inner +" "+ out
                print(inner)
            outer.append(inner)
