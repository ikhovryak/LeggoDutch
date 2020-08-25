import os

idx = 0
cur = "./finetune" 
for d in os.listdir(cur):
    
    if "ft" not in d:
        idx += 1
        os.rename(cur + "/" + d, cur + "/ft" + str(idx) + ".png")

