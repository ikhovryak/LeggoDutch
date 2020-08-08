from skimage import io, color
from scipy.fftpack import dct, idct
 
img = io.imread('./images/test_img.jpg')
gray = color.rgb2gray(img)
 
frequencies = dct(dct(gray, axis=0), axis=1)
frequencies[:2,:2] = 0
gray = idct(idct(frequencies, axis=1), axis=0)
 
gray = (gray - gray.min()) / (gray.max() - gray.min()) # renormalize to range [0:1]