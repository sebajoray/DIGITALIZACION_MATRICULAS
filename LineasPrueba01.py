# -*- coding: utf-8 -*-
"""
Created on Fri Jun 25 23:25:59 2021

@author: cesar
"""

# Python program to explain cv2.erode() method 
  
# importing cv2 
import cv2
  
# importing numpy 
import numpy as np
  
# path 
path = r'1-1-1-1838-.tif'
  
# Reading an image in default mode 
image = cv2.imread(path) 
 

# convierte la imagen en blanco y negro  y luego invierte para poder aplicar
# operaciones morfologicas como erosion. Queda fondo negro y lineas blancas
(T, imageBin) = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY_INV)


#altura aproximada de un caracter en pixeles
charAvgHeight = 32

# Kernel para erosionar de altura de un caracter. 
kernel = np.ones((charAvgHeight,1), np.uint8)
  
# aplica kernel dejando uniones de pixeles con longitud mayor a la de un caracter
# esto deja lineas horizontales si la imagen esta alineada a los margenes
#imageV = cv2.open(imageBin, kernel) 
imageV = cv2.morphologyEx(imageBin, cv2.MORPH_OPEN, kernel)

#aplica kernel transpuesto, solo deja lineas horizontales
imageH = cv2.morphologyEx(imageBin, cv2.MORPH_OPEN, kernel.T)
 
# combina las lineas horizontales y verticales. Intenta dejar solo la grilla 
imageOut = cv2.bitwise_or(imageV, imageH)

# invierte la imagen para obtener el fondo blanco y lineas negras
imageOut = 255-imageOut
# Displaying the image 
#cv2.imshow(window_name, image) 

cv2.imwrite(path+'-V.png', imageV)
cv2.imwrite(path+'-H.png', imageH)
cv2.imwrite(path+'-O.png', imageOut)
