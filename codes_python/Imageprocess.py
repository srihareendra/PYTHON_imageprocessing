import cv2
import numpy as np
from matplotlib import pyplot as plt
img =cv2.imread('my_drawing.jpg',0)
laplacian = cv2.Laplacian(img,cv2.CV_64F)
sobelx=cv2.Sobel(img,cv2.CV_64F,1,0,ksize=5)
sobely=cv2.Sobel(img,cv2.CV_64F,0,1,ksize=5)
print "hello"
plt.subplot(2,2,1),plt.imshow(img,cmap='gray')
plt.title('original'),plt.xticks([]),plt.yticks([])
print "hello"
plt.subplot(2,2,2),plt.imshow(laplacian,cmap='gray')
plt.title('laplacian'),plt.xticks([]),plt.yticks([])
plt.subplot(2,2,3),plt.imshow(sobelx,cmap='gray')
plt.title('sobelx'),plt.xticks([]),plt.yticks([])
plt.show()
print "hello"
