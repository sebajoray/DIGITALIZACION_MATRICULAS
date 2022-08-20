# import
from paddleocr import PaddleOCR
# inference
ocr = PaddleOCR(use_angle_cls=True, lang='es')
result = ocr.ocr('imagenes/image2.jpeg', cls=True)

for res in result:
    print(res[1][0]) 

