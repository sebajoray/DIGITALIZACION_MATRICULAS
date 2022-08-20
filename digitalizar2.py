# Importamos Pytesseract
import pytesseract
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv
# Importamos la libreria Pillow
# from PIL import Image
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


#read your file
file=r'felisarg2.tiff'
img = cv2.imread(file,0)

file=r'linea.tif'
img2 = cv2.imread(file,0)

rows,cols = img.shape

#thresholding the image to a binary image
thresh,img_bin = cv2.threshold(img, 180, 255, cv2.THRESH_BINARY_INV)

#inverting the image 
#img_bin = 255-img_bin

#Plotting the image to see the output

#result = cv2.fastNlMeansDenoisingColored(img,None,20,10,7,21)
#result=cv2.addWeighted(img, 2.5, np.zeros(img2.shape, img2.dtype), 0.5, 0)
#result=cv2.addWeighted(img2,0.5, np.zeros(img.shape, img.dtype),0.5,0)
result=cv2.addWeighted(img2[0:rows, 0:cols],0.5,img,0.5,0)



cv2.imwrite('result.png',result)
#plotting = plt.imshow(result,cmap='gray')
#plt.show()

# d = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)

# List of available languages
# print(pytesseract.get_languages(config=''))

archivo_salida = open('salida.txt', 'w')

opcion = 6

print(pytesseract.image_to_string(result, lang='spa', config=f'--psm {opcion}'), file = archivo_salida)

archivo_salida.close()

# Utilizamos el método "image_to_string"
# Le pasamos como argumento la imagen abierta con Pillow
# texto = pytesseract.image_to_string(im)

# Mostramos el resultado
# print(texto)


