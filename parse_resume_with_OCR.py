# -*- coding: utf8 -*-
# The program processes the PDF file and displays data that matches certain conditions. In this case:
# gender, growth, work experience and driver's license.

import fitz  # import pac. and lib.
import pytesseract
import matplotlib.pyplot as plt
import os
import sys

from pdf2image import convert_from_path, convert_from_bytes
from PIL import Image

def get_page_from_pdf(path_to_pdf):
    '''Данная функция считывает PDF файл по указанному пути и
        разбивает его на отдельные страницы
        input: путь
        return: список страниц, кол-во страниц'''
    list_image = []
    pdf = fitz.open(path_to_pdf)
    number_of_list = pdf.pageCount
    for page in pdf:
        pix = page.getPixmap(alpha = False, matrix=fitz.Matrix(300/100,300/100))
        mode = "RGBA" if pix.alpha else "RGB"
        img = Image.frombytes(mode, [pix.width, pix.height], pix.samples)
        list_image.append(img)
    return list_image, number_of_list


def conver_text_image(list_image):
    '''
    Функция принимает на вход список страниц и преобразует серый цвет
    шрифтов в чёрный для лучшего качества их распознавания.
    input:список страниц
    output: список конвертированных страниц
    '''
    convert_list_images = []

    for a in list_image:

        img = a.convert("RGBA")
        pixdata = img.load()
        for y in range(img.size[1]):
            for x in range(img.size[0]):
                if pixdata[x, y] != (255, 255, 255, 255):
                    pixdata[x, y] = (0, 0, 0, 255)

        convert_list_images.append(img)

    return convert_list_images



def find_target_page(conver_text_image):
    '''g'''
    data_of_pdf = []
    for x in conver_text_image:
        page_text = pytesseract.image_to_string(x, lang='rus').split('\n')
        search_text = ['родил', 'опыт работы', 'права']
        age = [i for i in page_text if search_text[0] in i.lower()]
        if age != []:
            data_of_pdf.append(age)

        skil_of_job = [i for i in page_text if search_text[1] in i.lower()]
        if skil_of_job != []:
            data_of_pdf.append(skil_of_job)

        have_a_car = [i for i in page_text if search_text[2] in i.lower()]
        if have_a_car != []:
            data_of_pdf.append(['Есть водительские права'])

    return data_of_pdf

def main_algorithm(**kwargs):
    path_to_pdf = kwargs['path']
    list_image, number_of_list = get_page_from_pdf(path_to_pdf)
    convert_color_of_text = find_target_page(conver_text_image(list_image))
    print (convert_color_of_text)


if __name__ == '__main__':

    print(sys.argv)
    try:
        path_to_image = sys.argv[1]

    except Exception as error:
        print(error)
        raise AttributeError

    main_algorithm(path=path_to_image)
