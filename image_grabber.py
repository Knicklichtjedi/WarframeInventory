from PIL import ImageGrab, ImageEnhance, ImageOps

image_path = './images/{}.png'.format


def grab_image(x, y, width, height, mates):
    # bbox specifies specific region (bbox= x,y,width,height *starts top-left)
    # img = Image.open(image_path('fissure_3'))
    img = ImageGrab.grab(bbox=(0, 0, 1920, 1080))

    img = ImageOps.autocontrast(img)
    img.save(image_path('capture_auto_c'))

    color = ImageEnhance.Color(img)
    img = color.enhance(0.0)
    img.save(image_path('capture_color'))

    # img = img.filter(ImageFilter.GaussianBlur(1))
    # img.save(image_path('capture_blur'))

    # sharpness = ImageEnhance.Sharpness(img)
    # img = sharpness.enhance(2.0)
    # img.save(image_path('capture_sharpen'))

    # contrast = ImageEnhance.Contrast(img)
    # img = contrast.enhance(2.0)
    # img.save(image_path('capture_contrast'))

    width_per_mate = width / 4
    for i in range(0, mates):
        moved_x = x + width_per_mate * i

        img_cropped = img.crop((moved_x, y, moved_x + width_per_mate, y + height))
        img_cropped.save(image_path('capture_{}'.format(i)))

        # ocr_result = image_reader.ocr(image_path('capture_{}'.format(i)))
        # boxes = ocr_result['boxes'].split('\n')
        # colors = ['red', 'yellow', 'green', 'blue']
        #
        # img_cap_box = Image.open(image_path('capture_{}'.format(i)))
        # img_cap_box = img_cap_box.transpose(Image.FLIP_TOP_BOTTOM)
        # draw = ImageDraw.Draw(img_cap_box)
        # for j, box in enumerate(boxes):
        #     content = box.split(' ')
        #
        #     if len(content) == 6:
        #         xb = int(content[1])
        #         yb = int(content[2])
        #         xb2 = int(content[3])
        #         yb2 = int(content[4])
        #
        #         draw.rectangle(((xb, yb), (xb2, yb2)), outline=colors[i])
        #
        # img_cap_box = img_cap_box.transpose(Image.FLIP_TOP_BOTTOM)
        # img_cap_box.save(image_path('capture_box_{}'.format(i)))

        # print('drawing {} boxes...'.format(len(boxes)))

    img_box = img.crop((x, y, x + width, y + height))
    img_box.save(image_path('capture'))

    return img
