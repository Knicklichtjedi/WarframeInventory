from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
image_path = './images/{}.png'.format


def optimize_text(text):
    separator = '_'
    special_characters = ['+', '*', '-', '_', '.', ':', ',', ';' '\"', '\'']

    text_blocks = text.split(' ')

    text_blocks = list(filter(lambda x: len(x) > 1, text_blocks))
    text_blocks = list(filter(lambda x: x not in special_characters, text_blocks))

    return separator.join(text_blocks)


def ocr(filename):
    """
    This function will handle the core OCR processing of images.
    """
    text = pytesseract.image_to_string(Image.open(filename), lang='eng')
    return {'text': optimize_text(text.replace('\n', ' ')), 'boxes': pytesseract.image_to_boxes(Image.open(filename))}
