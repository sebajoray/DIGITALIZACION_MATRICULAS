# import
from paddleocr import PaddleOCR
# inference
ocr = PaddleOCR(use_angle_cls=True, lang='es')
result = ocr.ocr('imagenes/1836 (015)/1-1-1-1836-.jpeg', cls=True)
concat_output = "\n".join(row[1][0] for row in result[0])
print(concat_output)
for res in result:
    print(res[1][0]) 

