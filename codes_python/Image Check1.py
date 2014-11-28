import tesseract
import cv2
import cv2.cv as cv

image0=cv2.imread("my_drawing.jpg")
#### you may need to thicken the border in order to make tesseract feel happy to ocr your image #####
offset=20
height,width,channel = image0.shape
image1=cv2.copyMakeBorder(image0,offset,offset,offset,offset,cv2.BORDER_CONSTANT,value=(255,255,255)) 
#cv2.namedWindow("Test")
#cv2.imshow("Test", image1)
#cv2.waitKey(0)
#cv2.destroyWindow("Test")
#####################################################################################################
api = tesseract.TessBaseAPI()
api.Init(".","eng",tesseract.OEM_DEFAULT)
api.SetPageSegMode(tesseract.PSM_AUTO)
height1,width1,channel1=image1.shape
print image1.shape
print image1.dtype.itemsize
width_step = width*image1.dtype.itemsize
print width_step
#method 1 
iplimage = cv.CreateImageHeader((width1,height1), cv.IPL_DEPTH_8U, channel1)
cv.SetData(iplimage, image1.tostring(),image1.dtype.itemsize * channel1 * (width1))
tesseract.SetCvImage(iplimage,api)

text=api.GetUTF8Text()
conf=api.MeanTextConf()
image=None
print "..............."
print "Ocred Text: %s"%text
print "Cofidence Level: %d %%"%conf

#method 2:
cvmat_image=cv.fromarray(image1)
iplimage =cv.GetImage(cvmat_image)
print iplimage

tesseract.SetCvImage(iplimage,api)
#api.SetImage(m_any,width,height,channel1)
text=api.GetUTF8Text()
conf=api.MeanTextConf()
image=None
print "..............."
print "Ocred Text: %s"%text
print "Cofidence Level: %d %%"%conf
api.End()
