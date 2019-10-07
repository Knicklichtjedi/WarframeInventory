from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
image_path = './images/{}.png'.format


def ocr(filename):
    """
    This function will handle the core OCR processing of images.
    """
    text = pytesseract.image_to_string(Image.open(filename), lang='eng')
    return {'text': text.replace('\n', ' '), 'boxes': pytesseract.image_to_boxes(Image.open(filename))}
