import pytesseract
import numpy as np 
import cv2 

def recognize(img, bboxes):

    (origH, origW) = img.shape[:2]
    results = []

    for idx, ([l, t], [r, t], [r, b], [l, b]) in enumerate(bboxes):

        poly = np.array(bboxes[idx]).astype(np.int32).reshape((-1))
        poly = poly.reshape(-1, 2)
        pts = poly.reshape((-1, 1, 2))
        
        ## (1) Crop the bounding rect
        rect = cv2.boundingRect(pts)
        x,y,w,h = rect
        roi = img[y:y+h, x:x+w].copy()

        ## (2) make mask
        pts = pts - pts.min(axis=0)

        mask = np.zeros(roi.shape[:2], np.uint8)
        cv2.drawContours(mask, [pts], -1, (255, 255, 255), -1, cv2.LINE_AA)

        ## (3) do bit-op
        dst = cv2.bitwise_and(roi, roi, mask=mask)

        ## (4) add the white background
        bg = np.ones_like(roi, np.uint8)*255
        cv2.bitwise_not(bg,bg, mask=mask)
        dst2 = bg+ dst


        # channel_count = roi.shape[2]  # i.e. 3 or 4 depending on your image
        # ignore_mask_color = (255,) * channel_count

        # cv2.fillPoly(mask, [poly.reshape((-1, 1, 2))], ignore_mask_color)
        # masked_image = cv2.bitwise_or(roi, mask)

        config = ("-l eng --oem 1 --psm 7")
        text = pytesseract.image_to_string(dst2, config=config)

        results.append((text, (l, r, t, b)))

        # cv2.imshow(text, dst2)
        # cv2.waitKey(0)

    return results





