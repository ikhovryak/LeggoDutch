import pytesseract

def recognize(img, bboxes):

    (origH, origW) = img.shape[:2]
    results = []

    for [l, t], [r, t], [r, b], [l, b] in boxes:
        
        mask = np.zeros(img.shape, dtype=np.uint8)

        # in order to obtain a better OCR of the text we can potentially
        # apply a bit of padding surrounding the bounding box -- here we
        # are computing the deltas in both the x and y directions
        dX = int((r - l))
        dY = int((b - t))

        # apply padding to each side of the bounding box, respectively
        l = max(0, l - dX)
        t = max(0, t - dY)
        r = min(origW, r + (dX * 2))
        b = min(origH, b + (dY * 2))

        # extract the actual padded ROI
        roi = img[t:b, l:r]

        poly = np.array(box).astype(np.int32).reshape((-1))
        poly = poly.reshape(-1, 2)

        channel_count = roi.shape[2]  # i.e. 3 or 4 depending on your image
        ignore_mask_color = (255,) * channel_count

        cv2.fillPoly(mask, [poly.reshape((-1, 1, 2))], ignore_mask_color)
        masked_image = cv2.bitwise_or(roi, mask)

        config = ("-l eng --oem 1 --psm 7")
        text = pytesseract.image_to_string(img, config=config)

        results.append((text, (l, r, t, b)))

    return results





