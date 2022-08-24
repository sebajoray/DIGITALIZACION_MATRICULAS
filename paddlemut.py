from paddleocr import PaddleOCR, draw_ocr # main OCR dependencies
from matplotlib import pyplot as plt # plot images
import cv2 #opencv
import os # folder directory navigation

# Setup model
ocr_model = PaddleOCR(lang='en')

img_path = os.path.join('.', '1-1-1-1838-.tif')

# Run the ocr method on the ocr model
result = ocr_model.ocr(img_path)

result

for res in result:
    print(res[1][0]) 