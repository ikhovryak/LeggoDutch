import cv2
import numpy as np 

img = cv2.imread("demo_1.jpg")

file = open("./res_demo_1.txt", "r")


for line in file.readlines():

    coords = line.split(",")
    # text = coords[-1]
    coords = [int(coord) for coord in coords]
    pts = np.array([[coords[0], coords[1]],
                    [coords[2], coords[3]],
                    [coords[4], coords[5]],
                    [coords[6], coords[7]]])

    rect = cv2.boundingRect(pts)
    x,y,w,h = rect
    croped = img[y:y+h, x:x+w].copy()

    pts = pts - pts.min(axis=0)

    mask = np.zeros(croped.shape[:2], np.uint8)
    cv2.drawContours(mask, [pts], -1, (255, 255, 255), -1, cv2.LINE_AA)
    dst = cv2.bitwise_and(croped, croped, mask=mask)

    # cv2.namedWindow("main", cv2.WINDOW_NORMAL)
    # cv2.resizeWindow('main', 800, 800)
    # cv2.imshow("main" ,dst)
    # cv2.waitKey(0)

    cv2.imwrite("./extracted_rois/{}_{}.png".format(x, y), dst)