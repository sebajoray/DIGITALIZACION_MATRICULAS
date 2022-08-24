from tesserocr import PyTessBaseAPI
images = ['felisarg2.tiff']
with PyTessBaseAPI(path='C:/Program Files/Tesseract-OCR/tessdata/.', lang='spa') as api:
    for img in images:
        api.SetImageFile(img)
        print(api.GetUTF8Text())