# Importamos Pytesseract
import pytesseract
import cv2
# Importamos la libreria Pillow
# from PIL import Image
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Abrimos la imagen
img_cv = cv2.imread(r'1-1-1-1838-.tif')
#cv2.threshold(img_cv, ) 

# d = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)

# List of available languages
# print(pytesseract.get_languages(config=''))


archivo_salida = open('output_1.txt', 'w')

opcion = 6

print(pytesseract.image_to_string(img_cv, lang='esp', config='--psm 6'), file = archivo_salida)
    
archivo_salida.close()

# Utilizamos el método "image_to_string"
# Le pasamos como argumento la imagen abierta con Pillow
# texto = pytesseract.image_to_string(im)

# Mostramos el resultado
# print(texto)


import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
tokens = nltk.word_tokenize(pytesseract.image_to_string(img_cv, lang='spa', config=f'--psm 6'))
tags = nltk.pos_tag(tokens)
nouns = [(word, tag) for word, tag in tags if tag in ['NNP', 'NNPS']]
print(nouns)