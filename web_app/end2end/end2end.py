from ..CRAFT import *
from ..deep_recognition import *
from pyteserract_engine import recognize
from preprocess_image import preprocess

def text_main_engine(image):

    dewarped = preprocess(image) # dewarp and deskew the image
    bboxes = craft_engine.predict(dewarped) # return predicted bounding boxes of text 

    # results = deep_recognize_engine.recognize(bboxes)
    #TODO: modify code in deep-text-recognize to experiment this text recognition engine
    # So far using pytesseract for text recognition in each predicted bounding box
    results = recognize(bboxes)

    #TODO: Implement same line bounding boxes of text with their coordinates 

    for idx in range(len(results)):
        for i in range(idx + 1, len(results)):
            
            top1 = results[idx][1][2]
            bot1 = results[idx][1][3]
            mid1 = (top1 + bot1) // 2
            range1 = bot1 - top1

            top2 = results[i][1][2]
            bot2 = results[i][1][3]
            mid2 = (top2 + bot2) // 2
            range2 = bot2 - top2

            if -10 < (range1 - range2) < 10:
                #do something
                print(results[idx], results[i])

    return results