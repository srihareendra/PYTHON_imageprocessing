import cv2
import numpy as np
from matplotlib import pyplot as plt
from skimage import feature
img = cv2.imread('my_drawing1.jpg',0)
edges = cv2.Canny(img,100,200)
edges2 = feature.canny(img, sigma=3)
plt.subplot(121),plt.imshow(img,cmap = 'gray')
plt.title('Original Image'), plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(edges2,cmap = 'gray')
plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

plt.show()
