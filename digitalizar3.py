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


for imagenes in ficheros:
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
    texto1 = pytesseract.image_to_string(imgtext, lang='spa', config=f'--psm 6')
    texto = texto1
    texto = re.sub(r'[^\da-záéíóúÁÉÍÓÚA-Z,; \n]+', ' ', texto)
    texto = re.sub(r'\n\s*\n', '\n', texto)
    texto = re.sub(r'[0-9]+', ' ', texto)
# elimino las lineas que no tengan atributos
    lineas_bien = []
    for linea in texto.split('\n'):
        #apellido = linea.split(',')
        #if len(apellido) > 1: 
        nombre = linea.split('arg')
        if len(nombre) > 0:
            print('persona:',nombre[0])
        for palabra in linea.split():
            largo_palabras = len(palabra)
            if (largo_palabras >= 3) and palabra.upper() not in nonombres:
                lineas_bien.append(palabra)



#elimino simbolos o palabras de menos de 1 caracter
    a_eliminar = re.compile(r'\W*\b\w{3}\b ')
    resultado = a_eliminar.sub('', "\n".join(lineas_bien))
    #print (resultado)

#print(ficheros)
#img_cv = cv2.imread(r'1-1-1-1838-.tif')
#cv2.threshold(img_cv, ) 

# d = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)

# List of available languages
# print(pytesseract.get_languages(config=''))


#archivo_salida = open('output_1.txt', 'w')

#opcion = 6

#print(pytesseract.image_to_string(img_cv, lang='spa', config='--psm 6'), file = archivo_salida)
    
#archivo_salida.close()

# Utilizamos el método "image_to_string"
# Le pasamos como argumento la imagen abierta con Pillow
# texto = pytesseract.image_to_string(im)

# Mostramos el resultado
# print(texto)


import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
tokens = nltk.word_tokenize(resultado)
tags = nltk.pos_tag(tokens)
nouns = [(word, tag) for word, tag in tags if tag in ['NNP', 'NNPS']]
print(nouns)