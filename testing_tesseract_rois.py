import cv2
import pytesseract
import imutils
import os

for f in os.listdir("./extracted_rois"):
    
    print(f)
    if f == ".DS_Store":
        continue
    
    img = cv2.imread("./extracted_rois/" + f, 0)
    # ret, img = cv2.threshold(img,110,255,cv2.THRESH_BINARY)
    
    config = ("-l eng --oem 1 --psm 8")
    text = pytesseract.image_to_string(img, config=config)

    cv2.imshow(text, img)
    cv2.waitKey(0)