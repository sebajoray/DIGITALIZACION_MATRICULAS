# Importamos Pytesseract
import pytesseract
import cv2
import os
from PIL import Image
from elasticsearch import Elasticsearch

es = Elasticsearch('http://localhost:9200', basic_auth=('seba', 'gemin8'), verify_certs=False)

# Importamos la libreria Pillow
# from PIL import Image
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Abrimos la imagen
path='/Users/User/proyectos/digitalizacion_matriculas/imagenes/imagen2'
with os.scandir(path) as ficheros:
    ficheros = [fichero.name for fichero in ficheros if fichero.is_file() and fichero.name.endswith('.jpeg')]

nonombres=['COPROPIEDAD', 'DECRETO', 'LEY','DECRETOLEY','BAHIA', 'LOTE', 'TERRENO', 'FEDERAL','ANTECEDENTE', 'PLANO',
'CANCELACIONES','TITULARIDAD','DPTO','MINISTERIO','HACIENDA','SIGUE','REGISTRO','PROVINCIA','RESTRICCIONES',
'EDIFICADO','UBICADO','CIUDAD','CALLE','APROBADO','SOBRE','DOMINIO','INTERDICCIONES','CANCELACIONES',
 'EMPLEADA', 'EMPLEADAS', 'EMPLEADO', 'EMPLEADOS','HIJO','HIJOS','HIJA','HIJAS','DEFINITIVA','BUENOS','AIRES',
 'DORSO', 'PROPIEDAD']


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

    imgtext = Image.open(filename)

    # limpio el codigo de caracteres que no corresponden
    texto1 = pytesseract.image_to_string(imgtext, lang='esp', config=f'--psm 6')
    print(texto1)
    es.index(
        index='matriculas',
        document={
        'path': path,
        'imagen': imagenes,
        'texto' : texto1

    })

print (es.info())