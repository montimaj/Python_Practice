from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import math

def read_image(img):
    img = Image.open(img)
    return img

def show_histogram(img, fig='1', bandwise=True):
    hist = img.histogram()
    plt.figure(fig)
    if bandwise:
        plt.subplot(311)
        plt.plot(hist[:256])
        plt.subplot(312)
        plt.plot(hist[256:512])
        plt.subplot(313)
        plt.plot(hist[512:768])
    else:
        plt.plot(hist)
    plt.show()

def invert_image(img, use_lib=False):
    if use_lib:
        return img.point(lambda x: 255-x)
    col, row = img.size
    for i in range(row):
        for j in range(col):
            r,g,b=img.getpixel((j,i))
            img.putpixel((j,i), (255-r,255-g,255-b))
    return img

def save_image(img, name):
    img.save(name)

def draw_lines(img):
    draw = ImageDraw.Draw(img)
    draw.line((0, 0) + img.size, fill=128)
    draw.line((0, img.size[1], img.size[0], 0), fill=128)
    return img

def scale_ndvi(ndvi):
    if ndvi<=0:
        return round(math.fabs(ndvi*128))
    return round(ndvi*128+127)

def generate_ndvi_image(rgbimg, nirimg):
    rimg=rgbimg.split()[0]
    nimg=nirimg.split()[0]
    ndvi_img=Image.new('L',rimg.size)
    cols, rows=rgbimg.size
    for i in range(rows):
        for j in range(cols):
            pos=(j,i)
            r=rimg.getpixel(pos)
            n=nimg.getpixel(pos)
            ndvi=0
            if n+r!=0:
                ndvi=(n-r)/(n+r)
            ndvi_img.putpixel(pos,(scale_ndvi(ndvi),))
    return ndvi_img

duckimg=read_image('Data/GI-Duck.jpg')
nirimg=read_image('Data/imagenir_new.tiff')
rgbimg=read_image('Data/imagergb.tiff')
#show_histogram(duckimg)
#show_histogram(nirimg,'2')
#invert_image(duckimg.copy(), True).show()
#draw_lines(duckimg).show()
#nirimg.show()
#rgbimg.show()
ndvi=generate_ndvi_image(rgbimg, nirimg)
show_histogram(ndvi, bandwise=False)
ndvi.show()
save_image(ndvi,'Data/ndvi.jpg')