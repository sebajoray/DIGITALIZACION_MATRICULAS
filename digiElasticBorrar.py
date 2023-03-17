# Importamos Pytesseract
import os
import pytesseract
from elasticsearch import Elasticsearch
from skimage import io


es = Elasticsearch('http://localhost:9200', basic_auth=('seba', 'gemin8'), verify_certs=False)

# Importamos la libreria Pillow
# from PIL import Image
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Abrimos la imagen
path='/Users/User/proyectos/digitalizacion_matriculas/imagenes/imagen2'
with os.scandir(path) as ficheros:
    ficheros = [fichero.name for fichero in ficheros if fichero.is_file() and fichero.name.endswith('.jpeg')]

nonombres=['COPROPIEDAD', 'DECRETO', 'LEY','DECRETOLEY','BAHIA', 'LOTE', 'TERRENO', 'FEDERAL','ANTECEDENTE', 'PLANO',
'CANCELACIONES','DPTO','MINISTERIO','HACIENDA','SIGUE','REGISTRO','PROVINCIA','RESTRICCIONES',
'EDIFICADO','UBICADO','CIUDAD','CALLE','APROBADO','SOBRE','DOMINIO','INTERDICCIONES','CANCELACIONES',
 'EMPLEADA', 'EMPLEADAS', 'EMPLEADO', 'EMPLEADOS','HIJO','HIJOS','HIJA','HIJAS','DEFINITIVA','BUENOS','AIRES',
 'DORSO', 'PROPIEDAD']


for imagenes in ficheros:
    print(imagenes)
    preprocess = "thresh"
    img = io.imread(path + "/" + imagenes)
#    cv2.imshow('imagen de la ruta', img)
    
    #cv2.imwrite(filename, gray)

    #imgtext = Image.open(filename)

    # limpio el codigo de caracteres que no corresponden
    texto1 = pytesseract.image_to_string(img, lang='font_name', config=f'--psm 6 --oem 1')
    print("-----------------------------------------------------------")
    print(texto1)
    texto = texto1.split('Titularidad')
    if len(texto) > 1:
        print('Texto:',texto[1])    
    

    """es.index(
        index='matriculas',
        document={
        'path': path,
        'imagen': imagenes,
        'texto' : texto1

    })"""

print (es.info())