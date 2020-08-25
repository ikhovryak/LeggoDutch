import os, sys; 
from pathlib import Path
import cv2
import re

import CRAFT
from CRAFT import craft_utils
from CRAFT import imgproc
from CRAFT import craft_engine

import deep_recognition
from deep_recognition import *
from pyteserract_engine import recognize
from preprocess_image import preprocess
from food_helper import if_food, line_food

def text_main_engine(image, weights_dir):

    lines = []

    dewarped = preprocess(image) # dewarp and deskew the image

    # cv2.imshow("main", dewarped)
    # cv2.waitKey(0)
    
    bboxes = craft_engine.predict(dewarped, trained_model = weights_dir) # return predicted bounding boxes of text 

    # results = deep_recognition.deep_recognize_engine.recognize(bboxes)
    #TODO: modify code in deep-text-recognize to experiment this text recognition engine
    # So far using pytesseract for text recognition in each predicted bounding box
    results = recognize(image, bboxes)


    #  ('W/Blk Pudding', (135.57208, 245.2455, 399.23886, 415.66885))
    # ('1.55', (380.0, 414.66666, 400.0, 417.33334))
    # range 1 -range2 = -1.5

    # ('1.55', (380.0, 414.66666, 400.0, 417.33334))
    # ('1 Breakfast Tea', (101.17823, 226.64772, 442.10788, 457.12082))

    for idx in range(len(results)):
        line = [results[idx][0]]

        for i in range(idx + 1, len(results)):
            
            top1 = results[idx][1][2]
            bot1 = results[idx][1][3]
            mid1 = (top1 + bot1) // 2
            range1 = bot1 - top1

            top2 = results[i][1][2]
            bot2 = results[i][1][3]
            mid2 = (top2 + bot2) // 2
            range2 = bot2 - top2

            if -5 < (mid1 - mid2) < 5:
                
                line.append(results[i][0])
                word = results[i][0].split()

        lines.append(line)

    lines = [line for line in lines if line_food(line)] 
    
    dish_dict = dict()
    for line in lines:
        dish_dict[line[0]] = line[-1]

    return dish_dict

if __name__ == '__main__':

    image = CRAFT.imgproc.loadImage("./demo/image_23.png")
    res = text_main_engine(image)
    print(res)