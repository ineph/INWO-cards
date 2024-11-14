import os
import math
import numpy
import matplotlib.pyplot as plt

from paddleocr import PaddleOCR, draw_ocr
from PIL import Image

img_path = 'D:/Games/illuminati/2/Illuminati - New World Order/INWO - Base/BASE-cards'
output_path = ''
excluded_keywords = [
    'ORDER',
    'NEW WORLD',
    'NEW WORLD',
    'NEW WORLD ORDER',
    'NEWWORLD ORDER',
    'NEWWORLDORDER',
    'NEW WORLDORDER'
    'PLACE',
    'GOAL',
]


def write_to_file(card_name, list_of_text_lines, where_to_save):
    #title = list_of_text_lines[0]
    #if title in list_of_text_lines and len(list_of_text_lines) > 1:
    #    title = list_of_text_lines[1]

    file_name = f'{where_to_save}/{card_name}.txt'
    
    if '?' in file_name:
        with open('invalid cards', "a") as f:
            f.write('###############################\n')
            f.write('###############################\n')
            f.write(file_name + '\n')
            f.write('vvvvvvv\n')
            for line in list_of_text_lines:    
                f.write(line + '\n')

    with open(file_name, "a") as f:
        for line in list_of_text_lines:

            f.write(line + '\n')


def is_light_background(text, color, light_threshold=(200, 255), gray_range=(180, 220)):
    r, g, b = color
    is_white_like = all(light_threshold[0] <= x <= light_threshold[1] for x in (r, g, b))
    is_gray_like = all(gray_range[0] <= x <= gray_range[1] for x in (r, g, b))
    return is_white_like or is_gray_like

def check_bg_color(bbox, np_image):
    height, width, _ = np_image.shape
    bg_color = None
    x1, y1, x2, y2 = int(bbox[0][0]), int(bbox[0][1]), int(bbox[1][0]), int(bbox[1][1])
    x1, y1 = max(0, min(x1, width - 1)), max(0, min(y1, height - 1))
    x2, y2 = max(0, min(x2, width - 1)), max(0, min(y2, height - 1))
    if x1 <= x2 and y1 <= y2:
        bg_color = np_image[y1:y2, x1:x2].mean(axis=(0, 1))
    else:   
        bg_color = None
    return bg_color

def dive():
    for root, _, files in os.walk(img_path):
        for file in files:
            if file.lower().endswith('.png'):
                full_img_path = os.path.join(root, file)
                card_name, card_text = process_image(full_img_path)
                write_to_file(card_name, card_text, root)


def process_image(img_path):
    card_name = os.path.splitext(os.path.basename(img_path))[0]

    ocr = PaddleOCR(use_angle_cls=False, lang='en')
    result = ocr.ocr(
        img_path,
        cls=False,
    )

    #light_threshold=(200, 255)
    #gray_range=(180, 220)

    text_lines = []
    for bbox, line in result[0]:
        text = line[0]
        accuracy = line[1]

#        if text not in excluded_keywords:


        print(f"¬{text} |  {accuracy}")
        text_lines.append(text)
    return card_name, text_lines


dive()


#image = Image.open(img_path).convert('RGB')
#boxes = [elements[0] for elements in result[0]]
#txts = [elements[1][0] for elements in result[0]]
#scores = [elements[1][1] for elements in result[0]]
#im_show = draw_ocr(image, boxes, txts, scores, font_path='C:Windows/Fonts/Arial.ttf')
#
#plt.imshow(im_show)
#plt.axis('off')
#plt.show()
