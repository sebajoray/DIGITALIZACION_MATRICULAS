# Importamos Pytesseract
import pytesseract
import cv2
import os
from PIL import Image
import re
# Importamos la libreria Pillow
# from PIL import Image
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Abrimos la imagen
path='/Users/User/proyectos/digitalizacion_matriculas/imagenes'
with os.scandir(path) as ficheros:
    ficheros = [fichero.name for fichero in ficheros if fichero.is_file() and fichero.name.endswith('.jpeg')]

nonombres=['COPROPIEDAD', 'DECRETO', 'LEY','DECRETOLEY','BAHIA', 'LOTE', 'TERRENO', 'FEDERAL','ANTECEDENTE', 'PLANO',
'CANCELACIONES','TITULARIDAD','DPTO','MINISTERIO','HACIENDA','SIGUE','REGISTRO','PROVINCIA','RESTRICCIONES',
'EDIFICADO','UBICADO','CIUDAD','CALLE','APROBADO','SOBRE','DOMINIO','INTERDICCIONES','CANCELACIONES',
 'EMPLEADA', 'EMPLEADAS', 'EMPLEADO', 'EMPLEADOS','HIJO','HIJOS','HIJA','HIJAS','DEFINITIVA','BUENOS','AIRES',
 'DORSO', 'PROPIEDAD']

from paddleocr import PaddleOCR
# inference
ocr = PaddleOCR(use_angle_cls=True, lang='es')

for imagenes in ficheros:
    print(imagenes)
    preprocess = "thresh"
    img = cv2.imread(path + "/" + imagenes)
#    cv2.imshow('imagen de la ruta', img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    if (preprocess == "thresh"):
        gray = cv2.threshold(
            gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    elif (preprocess == "blur"):
        gray = cv2.medianBlur(gray, 3)
    filename = "{}.png".format(os.getpid())
    cv2.imwrite(filename, gray)

    #imgtext = Image.open(filename)

    # limpio el codigo de caracteres que no corresponden
    #texto1 = pytesseract.image_to_string(imgtext, lang='typewriter', config=f'--psm 6')
    texto1 = ocr.ocr(path + "/" + imagenes, cls=True)
    for res in texto1:
        print(res[1][0]) 
    texto = texto1
    texto = re.sub(r'[^\da-záéíóúÁÉÍÓÚA-Z,; \n]+', ' ', texto)
    texto = re.sub(r'\n\s*\n', '\n', texto)
    texto = re.sub(r'[0-9]+', ' ', texto)
# elimino las lineas que no tengan atributos
    for linea in texto.split('\n'):
        #apellido = linea.split(',')
        #if len(apellido) > 1: 
        nombre = linea.split('arg')
        if len(nombre) > 1:
            print('persona:',nombre[0])

