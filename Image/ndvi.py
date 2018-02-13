from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import numpy as np
from osgeo import gdal

def read_image(img, bit=8):
    if bit<=8:
        img = Image.open(img)
    else:
        img = gdal.Open(img)
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

def scale_ndvi(ndvi, bit=8):
    scale_factor=2**(bit - 1)
    if ndvi<=0:
        return int(round(np.abs(ndvi*scale_factor)))
    return round(ndvi*scale_factor+scale_factor-1)

def generate_ndvi_image(rgbimg, nirimg):
    rimg=rgbimg.split()[0]
    nimg=nirimg.split()[0]
    ndvi_img=Image.new('L',rimg.size)
    cols, rows=rgbimg.size
    for i in range(rows):
        for j in range(cols):
            pos=(j,i)
            r=float(rimg.getpixel(pos))
            n=float(nimg.getpixel(pos))
            ndvi=0.
            d=n+r
            if d != 0:
                num=n-r
                ndvi=num/d
            ndvi_img.putpixel(pos,(scale_ndvi(ndvi, 8),))
    return ndvi_img

def save_img_16(input_img, arr_out, outfile):
    cols,rows=input_img.shape
    driver = gdal.GetDriverByName("GTiff")
    outdata = driver.Create(outfile, rows, cols, 1, gdal.GDT_UInt16)
    #outdata.SetGeoTransform(input_img.GetGeoTransform())  ##sets same geotransform as input
    #outdata.SetProjection(input_img.GetProjection())  ##sets same projection as input
    outdata.GetRasterBand(1).WriteArray(arr_out)
    #outdata.GetRasterBand(1).SetNoDataValue(10000)  ##if you want these values transparent
    outdata.FlushCache()
    
def generate_ndvi_image_16(rgbimg, nirimg):
    rimg=rgbimg.GetRasterBand(1).ReadAsArray()
    nimg=nirimg.GetRasterBand(1).ReadAsArray()
    cols, rows = rimg.shape
    outarr = np.zeros(shape=rimg.shape)
    for i in range(rows):
        for j in range(cols):
            r=float(rimg[j][i])
            n=float(nimg[j][i])
            ndvi=0.
            d=n+r
            if d!=0:
                num=n-r
                ndvi=num/d
            outarr[j][i]=scale_ndvi(ndvi, 16)
    return rimg, outarr

'''
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
save_image(ndvi,'Outputs/ndvi_8.jpg')
'''
nirimg=read_image(r'Data/ikonos-nir.tif')
rgbimg=read_image(r'Data/ikonos-rgb.tif')
ndvi=generate_ndvi_image(rgbimg, nirimg)
save_image(ndvi, 'Outputs/ndvi_8.tif')
nirimg=read_image(r'Data/ikonos-nir.tif', 16)
rgbimg=read_image(r'Data/ikonos-rgb.tif', 16)
rimg, ndvi_arr= generate_ndvi_image_16(rgbimg, nirimg)
save_img_16(rimg,ndvi_arr,'Outputs/ndvi_16.tif')