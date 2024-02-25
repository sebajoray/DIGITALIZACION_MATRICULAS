# Importamos Pytesseract
from paddleocr import PaddleOCR# main OCR dependencies
import cv2
import os
from os import remove
import img2pdf
from elasticsearch import Elasticsearch
from pathlib import Path
from skimage import io
import shutil
import aspose.words as aw
from PIL import Image
import re


es = Elasticsearch('http://localhost:9200', basic_auth=('seba', 'gemin8'), verify_certs=False)

# Importamos la libreria Pillow
# from PIL import Image
ocr_model = PaddleOCR(lang='en')
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
        nombrePdf = ruta.replace("-", "_").replace("(", "_").replace(")", "").replace(" ", "")
        if not os.path.isfile(nombrePdf+".pdf"):
            with open(nombrePdf+".pdf", "wb") as documento:
    	        documento.write(img2pdf.convert(imgs))
        for g in imgs:
            remove(g)
        imgs=[]
            #img = io.imread("1-1-1-1836-.tif")

file_destination = '/Users/User/proyectos/digitalizacion_matriculas/static'
 
get_files = os.listdir(path)
 
for g in get_files:
    if g.endswith('pdf') and not Path(file_destination + '/' + g).is_file():
        shutil.move(path + '/' + g, file_destination)

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

    rubroA = anteDom = descrip = nroInscri = ""
    
#    cv2.imshow('imagen de la ruta', img)
    
    gray = cv2.medianBlur(img,5)
    #if (preprocess == "thresh"):
    #   gray = cv2.threshold(
    #        gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    if (preprocess == "blur"):
        gray = cv2.medianBlur(gray, 3)
    filename = "{}.png".format(os.getpid())
    #cv2.imwrite(filename, gray)

    #imgtext = Image.open(filename)

    # limpio el codigo de caracteres que no corresponden
    result = ocr_model.ocr(img)
    print("-----------------------------------------------------------")
    texto1 = "\n".join(row[1][0] for row in result[0])
    print(texto1)
    def custom_split(sepr_list, str_to_split):
        # create regular expression dynamically
        regular_exp = '|'.join(map(re.escape, sepr_list))
        return re.split(regular_exp, str_to_split)
    separadores = ["Titularidad","TITULARIDAD","Gravámenes", "GRAVAMENES", "GRAVÁMENES",
                "Interdicciones","INTERDICCIONES","CANCELACIONES","Cancelaciones",
                "Restricciones","RESTRICCIONES","Certificaciones","CERTIFICACIONES"]
    catastro = ["Catastro", "CATASTRO"]
    antecedentes = ["antecedentes", "Antecedentes","ANTECEDENTES", "DOMINIALES", "dominiales", "Dominiales"]

    texto = custom_split(separadores, texto1)
    if len(texto) > 1:
        #texto1 es el contenido de las columnas
        descrip=texto[0]
    rubroA = texto[-1]

    texto = texto[0]
    catastro = custom_split(catastro,texto)
    if len(catastro) > 1:
        print("Encontro CATASTRO ---------------------------------")
        nroInscri = catastro[0]     
        texto = catastro[1]
    else:
        print(catastro[0])
    antecedente = custom_split(antecedentes, texto)
    if len(antecedente) > 1:
        if len(rubroA) > 0:
            anteDom = antecedente[1]

    print("*********descrip", descrip)
    es.index(
        index='matriculas3',
        document={
        'path': par[0],
        'imagen': par[1],
        'nroInscri' : nroInscri,
        'anteDom': anteDom,
        'rubroA' : rubroA,
        'descrip' : descrip
    })


