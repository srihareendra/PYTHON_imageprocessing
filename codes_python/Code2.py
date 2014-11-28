from PIL import Image, ImageChops
import cv2
def trim(im):
    bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)

im1 = Image.open("my_drawing.jpg")
im2 = trim(im1)
filename = "my_drawing1.jpg"
im2.save(filename)

