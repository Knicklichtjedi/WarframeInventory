import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageGrab
from matplotlib import pyplot as plt

import image_reader

image_path = './images/{}.png'.format
fissure_path = './fissures/{}.png'.format
BINARY_THRESHOLD = 255


def image_rescaling(img):
    length_x, width_y = img.size
    factor = min(1, float(1024.0 / length_x))
    size = int(factor * length_x), int(factor * width_y)
    im_resized = img.resize(size, Image.ANTIALIAS)
    return im_resized


def image_smoothening(img):
    ret1, th1 = cv2.threshold(img, BINARY_THRESHOLD, 255, cv2.THRESH_BINARY)
    ret2, th2 = cv2.threshold(th1, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    blur = cv2.GaussianBlur(th2, (5, 5), 0)
    ret3, th3 = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    cv2.imwrite(image_path('capture_smooth'), img)
    return th3


def image_binarization(img):
    img = cv2.medianBlur(img, 3)

    # blockSize Size of a pixel neighborhood that is used to calculate a threshold value for the.
    # pixel: 3, 5, 7, and so on.

    # C Constant subtracted from the mean or weighted mean (see the details below). Normally, it. is positive but may be
    # zero or negative as well.
    filtered = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, blockSize=11, C=7)
    cv2.imwrite(image_path('capture_filtered'), filtered)

    # http://www9.in.tum.de/seminare/ps.SS06.gdbv/ausarbeitungen/psbv-ss06-morphologie-karakoc.pdf
    # https://docs.opencv.org/trunk/d9/d61/tutorial_py_morphological_ops.html
    kernel = np.ones((2, 2), np.uint8)
    opening = cv2.morphologyEx(filtered, cv2.MORPH_OPEN, kernel)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)

    img = image_smoothening(img)
    or_image = cv2.bitwise_or(img, closing)
    return or_image


def grab_image(x, y, width, height, mates):
    # bbox specifies specific region (bbox= x,y,width,height *starts top-left)
    # img = Image.open(fissure_path('fissure_0')).crop((x, y, x + width, y + height))
    img = ImageGrab.grab(bbox=(x, y, x + width, y + height))

    img = image_rescaling(img)
    img.save(image_path('capture_raw'), dpi=(300, 300))

    # CONVERT TO NUMPY ARRAY
    img = np.array(img)
    # img = cv2.imread(image_path('capture_raw', 0))

    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.bitwise_not(img)
    img = image_binarization(img)

    cv2.imwrite(image_path('capture_preprocessed'), img)

    # CONVERT TO PIL OBJECT
    img = Image.fromarray(img)
    # img = Image.open(image_path('capture_preprocessed'))

    width_per_mate = width / 4
    for i in range(0, mates):
        moved_x = 0 + width_per_mate * i

        img_cropped = img.crop((moved_x, 0, moved_x + width_per_mate, 0 + height))
        img_cropped.save(image_path('capture_{}'.format(i)))

        ocr_result = image_reader.ocr(image_path('capture_{}'.format(i)))

        boxes = ocr_result['boxes'].split('\n')
        colors = ['red', 'yellow', 'green', 'blue']

        img_cap_box = Image.open(image_path('capture_{}'.format(i))).convert('RGB')
        img_cap_box = img_cap_box.transpose(Image.FLIP_TOP_BOTTOM)
        draw = ImageDraw.Draw(img_cap_box)
        for j, box in enumerate(boxes):
            content = box.split(' ')

            if len(content) == 6:
                xb = int(content[1])
                yb = int(content[2])
                xb2 = int(content[3])
                yb2 = int(content[4])

                draw.rectangle(((xb, yb), (xb2, yb2)), outline=colors[i])

        img_cap_box = img_cap_box.transpose(Image.FLIP_TOP_BOTTOM)
        img_cap_box.save(image_path('capture_box_{}'.format(i)))

        print('drawing {} boxes...'.format(len(boxes)))
