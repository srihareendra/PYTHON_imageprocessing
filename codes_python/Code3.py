import cv2

import cv2.cv as cv
import tesseract
img = cv2.imread('my_drawing.jpg',0)
ret1,th1 = cv2.threshold(img,90,255,cv2.THRESH_BINARY)


api = tesseract.TessBaseAPI()
api.Init(".","eng",tesseract.OEM_DEFAULT)
api.SetPageSegMode(tesseract.PSM_AUTO)
cv2.imwrite("images20.jpg",th1)
image=cv.LoadImage("images20.jpg", cv.CV_LOAD_IMAGE_GRAYSCALE)
tesseract.SetCvImage(image,api)
text=api.GetUTF8Text()
conf=api.MeanTextConf()
print text

api.End()
