# Importamos Pytesseract
import pytesseract
import cv2
import os
import img2pdf
from elasticsearch import Elasticsearch
from pathlib import Path
from skimage import io
import aspose.words as aw
from PIL import Image


es = Elasticsearch('http://localhost:9200', basic_auth=('seba', 'gemin8'), verify_certs=False)

# Importamos la libreria Pillow
# from PIL import Image
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Abrimos la imagen
path='/Users/User/proyectos/digitalizacion_matriculas/imagenes'
lista=[]
imgs=[]
for ruta, directorios, ficheros in os.walk(path):
    print(f'\nDirectorio: {ruta}')
    doc = aw.Document()
    builder = aw.DocumentBuilder(doc)
    for fichero in ficheros:

        lista.append([ruta, fichero])
        img = io.imread(os.path.join(ruta, fichero))
        io.imsave(os.path.join(ruta, fichero)+".jpg", img)
 #       builder.insert_image(os.path.join(ruta, fichero)+".jpg")
        # Insert a paragraph break to avoid overlapping images.
 #       builder.writeln()
        imgs.append(os.path.join(ruta, fichero)+".jpg")
    print('imagenes:', imgs)
    print('ficheros:', ficheros)
    if lista:
#        doc.save(ruta+".pdf")
        with open(ruta+".pdf", "wb") as documento:
    	    documento.write(img2pdf.convert(imgs))
            #img = io.imread("1-1-1-1836-.tif")
nonombres=['COPROPIEDAD', 'DECRETO', 'LEY','DECRETOLEY','BAHIA', 'LOTE', 'TERRENO', 'FEDERAL','ANTECEDENTE', 'PLANO',
'CANCELACIONES','DPTO','MINISTERIO','HACIENDA','SIGUE','REGISTRO','PROVINCIA','RESTRICCIONES',
'EDIFICADO','UBICADO','CIUDAD','CALLE','APROBADO','SOBRE','DOMINIO','INTERDICCIONES','CANCELACIONES',
 'EMPLEADA', 'EMPLEADAS', 'EMPLEADO', 'EMPLEADOS','HIJO','HIJOS','HIJA','HIJAS','DEFINITIVA','BUENOS','AIRES',
 'DORSO', 'PROPIEDAD']

for par in lista:
    
 #   print(imagenes)
    preprocess = "thresh"
    fichero = par[0] + "\\" + par[1]
    print('archivo: ', fichero)

    img = io.imread(fichero)
#    cv2.imshow('imagen de la ruta', img)
    #gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #if (preprocess == "thresh"):
    #    gray = cv2.threshold(
    #        gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    #elif (preprocess == "blur"):
    #    gray = cv2.medianBlur(gray, 3)
    #filename = "{}.png".format(os.getpid())
    #cv2.imwrite(filename, gray)

    #imgtext = Image.open(filename)

    # limpio el codigo de caracteres que no corresponden
    texto1 = pytesseract.image_to_string(img, lang='font_name', config=f'--psm 6 --oem 1')
    print("-----------------------------------------------------------")
    texto = texto1.split('Titularidad')
    if len(texto) > 1:
        texto1=texto[1]
    print('Texto:',texto1)    
    es.index(
        index='matriculas2',
        document={
        'path': par[0],
        'imagen': par[1],
        'texto' : texto1

    })
