from PIL import Image
import os, sys

idx = 0
for d in os.listdir("./"):
    # print(d)
    if ".jpg" in d or ".jpeg" in d:

        im = Image.open(d)
        im.save("image_" + str(idx) + ".png")
        idx += 1

