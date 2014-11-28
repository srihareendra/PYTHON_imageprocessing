import numpy as np
import matplotlib.pyplot as plt

from skimage import img_as_ubyte
from skimage import data

noisy_image = img_as_ubyte(data.camera())
hist = np.histogram(noisy_image, bins=np.arange(0, 256))

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 3))
ax1.imshow(noisy_image, interpolation='nearest', cmap=plt.cm.gray)
ax1.axis('off')
ax2.plot(hist[1][:-1], hist[0], lw=2)
ax2.set_title('Histogram of grey values')
