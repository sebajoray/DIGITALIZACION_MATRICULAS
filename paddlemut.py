from paddleocr import PaddleOCR# main OCR dependencies
from matplotlib import pyplot as plt # plot images
import cv2 #opencv
import os # folder directory navigation

# Setup model
ocr_model = PaddleOCR(lang='en')

img_path = os.path.join('imagenes/1836 (015)/1-1-1-1836-.jpeg')

# Run the ocr method on the ocr model
result = ocr_model.ocr(img_path)

result

for res in result:
    print(res[1][0]) 