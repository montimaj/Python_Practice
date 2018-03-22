from osgeo import gdal
import numpy as np

def read_image(img):
    return gdal.Open(img)

def get_covariance(x, y):
    x = x.tolist()[0]
    y = y.tolist()[0]
    mx = np.mean(x)
    my = np.mean(y)
    cov = 0
    for i, j in zip(x,y):
        cov += (i-mx)*(j-my)
    cov /= (len(x)-1)
    return cov

def resize_img(x, y):
    sizex = min(x.shape[0], y.shape[0])
    sizey = min(x.shape[1], y.shape[1])
    x = x[:sizex, :sizey]
    y = y[:sizex, :sizey]
    x = x.reshape(1, sizex * sizey)
    y = y.reshape(1, sizex * sizey)
    return x, y

def get_corrcoef(img1, img2):
    corrcoefs = []
    for band in range(1, img1.RasterCount + 1):
        x = img1.GetRasterBand(band).ReadAsArray()
        y = img2.GetRasterBand(band).ReadAsArray()
        x, y = resize_img(x, y)
        corrcoefs.append(np.corrcoef(x, y)[0, 1])
    return corrcoefs

def get_rmse(ref, img):
    rmse = []
    for band in range(1, ref.RasterCount + 1):
        x = ref.GetRasterBand(band).ReadAsArray()
        y = img.GetRasterBand(band).ReadAsArray()
        x, y = resize_img(x, y)
        rmse.append(np.sqrt(np.mean((x-y)**2)))
    return rmse

def get_relative_mean(ref, img):
    meansx = []
    meansy = []
    for band in range(1, ref.RasterCount + 1):
        meansx.append(np.mean(ref.GetRasterBand(band).ReadAsArray()))
        meansy.append(np.mean(img.GetRasterBand(band).ReadAsArray()))
    meansx = np.matrix(meansx)
    meansy = np.matrix(meansy)
    diff = meansx - meansy
    return np.linalg.norm(diff)

def get_entropy(img):
    entropy = []
    for band in range(1, img.RasterCount + 1):
        data = img.GetRasterBand(band).ReadAsArray()
        data  = data.reshape((1, data.shape[0]*data.shape[1]))
        data = data.tolist()[0]
        v = 0.
        for val in data:
            if val > 0:
                v += -val*np.log2(val)
        entropy.append(v)
    return -np.linalg.norm(entropy)

def image_quality_index(ref, img):
    qi = []
    for band in range(1, ref.RasterCount + 1):
        x = ref.GetRasterBand(band).ReadAsArray()
        y = img.GetRasterBand(band).ReadAsArray()
        x, y = resize_img(x, y)
        varx = np.var(x)
        vary = np.var(y)
        meanx = np.mean(x)
        meany = np.mean(y)
        print("MX=", meanx, "MY=", meany)
        num = 4. * get_covariance(x, y) * meanx * meany
        denom = (varx + vary) * (meanx ** 2 + meany ** 2)
        val = num/denom
        qi.append(val)
    return qi

def do_analysis(multispec, image, fp):
    fp.write("IMAGE = " + image.GetDescription() + "\n")
    qi = image_quality_index(multispec, image)
    for (index, q) in enumerate(qi):
        fp.write("Image Quality Band # " + str(index + 1) + " = " + str(q) + "\n")
    rmse = get_rmse(multispec, image)
    for (index, r) in enumerate(rmse):
        fp.write("RMSE Band # " + str(index + 1) + " = " + str(r) + "\n")
    fp.write("Relative mean = " + str(get_relative_mean(multispec, image)) + "\n")
    fp.write("Entropy = " + str(get_entropy(image)) + "\n")
    corrcoefs = get_corrcoef(multispec, image)
    print(corrcoefs)
    fp.write("Corrcoef between " + multispec.GetDescription() + " and " + image.GetDescription() + "\n")
    for (index, c) in enumerate(corrcoefs):
        fp.write("Band #" + str(index + 1) + "= " + str(c) + "\n")
    for img in images:
        if image != img:
            fp.write("Corrcoef between " + image.GetDescription() + " and " + img.GetDescription() + "\n")
            corrcoefs = get_corrcoef(image, img)
            for (index, c) in enumerate(corrcoefs):
                fp.write("Band #" + str(index + 1) + "= " + str(c) + "\n")
    fp.write("\n")

multispec = read_image(r"D:/M8/Fusion_prac_data/optical_fusion_data/xs_subiko.img")

pcfused = read_image(r"D:/M8/Fusion_prac_data/Fused_New/pcfused.img")
broveyfused = read_image(r"D:/M8/Fusion_prac_data/Fused_New/broveyfused.img")
mulfused = read_image(r"D:/M8/Fusion_prac_data/Fused_New/mulfused.img")
hpffused = read_image(r"D:/M8/Fusion_prac_data/fused/hpffused.img")
ihsfused = read_image(r"D:/M8/Fusion_prac_data/fused/ihsfused.img")
ehlrsfused = read_image(r"D:/M8/Fusion_prac_data/Fused_New/ehlrsfused.img")
waveletfused = read_image(r"D:/M8/Fusion_prac_data/fused/waveletfused.img")
images = [pcfused, broveyfused, mulfused, hpffused, ihsfused, ehlrsfused, waveletfused]

fp = open("Out.txt", "w")
for image in images[1:2]:
    do_analysis(multispec, image, fp)
fp.close()