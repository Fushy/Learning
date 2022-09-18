# pip install pillow pytesseract googletrans==3.1.0
# pip install translate-api
# https://nanonets.com/blog/ocr-with-tesseract/#tesseract-ocr
from PIL import Image
import pytesseract
from googletrans import Translator

if __name__ == '__main__':
    pytesseract.pytesseract.tesseract_cmd = r'B:\Programmes\Tesseract-OCR\tesseract.exe'
    img = Image.open('a.png')
    result = pytesseract.image_to_string(img)
    print(result)
