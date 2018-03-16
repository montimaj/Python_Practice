'''
from osgeo import gdal
import numpy as np
from collections import defaultdict
import matplotlib.pyplot as plt

def read_image(img):
    return gdal.Open(img)

def get_corrcoef(img1, img2, band_no):
    b1 = np.concatenate(img1.GetRasterBand(band_no).ReadAsArray())
    b2 = np.concatenate(img2.GetRasterBand(band_no).ReadAsArray())
    return np.corrcoef(b1, b2)

def display_corrcoeffs(images):
    n = len(images)
    for i in range(n):
        for j in range(n):
            if i!=j:
                for k in range(3):
                    print("Corrcoeff(" + str(i+1) + "," + str(j+1) + ";" + str(k+1) +")= ", get_corrcoef(images[i], images[j], k+1))

def display_hist(img, band_no):
    arr = img.GetRasterBand(band_no).ReadAsArray()
    hist = defaultdict(lambda: 0)
    for i in range(arr.shape[1]):
        for j in range(arr.shape[0]):
            hist[arr[j,i]] = hist[arr[j,i]] + 1
    keys = list(hist.keys())
    values = list(hist.values())
    keys = np.linspace(min(keys), max(keys), 10000)
    values = np.linspace(min(values), max(values), 10000)
    plt.hist(np.clip(arr, 0, 256), bins=20)


pcfused = read_image(r"D:/M8/Fusion_prac_data/fused/pcfused.img")
broveyfused = read_image(r"D:/M8/Fusion_prac_data/fused/broveyfused.img")
mulfused = read_image(r"D:/M8/Fusion_prac_data/fused/mulfused.img")
hpffused = read_image(r"D:/M8/Fusion_prac_data/fused/hpffused.img")
ihsfused = read_image(r"D:/M8/Fusion_prac_data/fused/ihsfused.img")
images = [pcfused, broveyfused, mulfused, hpffused, ihsfused]
#display_corrcoeffs(images[-2:])
display_hist(broveyfused, 1)

from pykml import parser
kml_str = '<kml xmlns="http://www.opengis.net/kml/2.2">' \
                 '<Document>' \
                   '<Folder>' \
                   '<name>sample folder</name>' \
                   '</Folder>' \
                 '</Document>' \
                '</kml>'
root = parser.fromstring(kml_str)
print root.Document.Folder.name.text

'''