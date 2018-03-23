from osgeo import gdal
import numpy as np
import os
from threading import Thread

def read_image(img):
    return gdal.Open(img)

def get_covariance(x, y):
    x = x.tolist()
    y = y.tolist()
    mx = np.mean(x)
    my = np.mean(y)
    cov = 0
    for i, j in zip(x, y):
        cov += (i - mx) * (j - my)
    cov /= (len(x) - 1)
    return cov

def resize_img(x, y):
    sizex = min(x.shape[0], y.shape[0])
    sizey = min(x.shape[1], y.shape[1])
    x = x[:sizex, :sizey]
    y = y[:sizex, :sizey]
    x = x.reshape(sizex * sizey)
    y = y.reshape(sizex * sizey)
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
        rmse.append(np.sqrt(np.mean((x - y) ** 2)))
    return rmse

def get_relative_mean(ref, img):
    meansx = []
    meansy = []
    for band in range(1, ref.RasterCount + 1):
        meansx.append(np.mean(ref.GetRasterBand(band).ReadAsArray()))
        meansy.append(np.mean(img.GetRasterBand(band).ReadAsArray()))
    meansx = np.array(meansx)
    meansy = np.array(meansy)
    diff = np.abs((meansx - meansy)/meansx)
    return diff, np.linalg.norm(diff)

def get_entropy(img):
    entropy = []
    for band in range(1, img.RasterCount + 1):
        data = img.GetRasterBand(band).ReadAsArray()
        data  = data.reshape(data.shape[0] * data.shape[1])
        data = data.tolist()
        dn, counts = np.unique(data, return_counts = True)
        counts = counts / len(data)
        dn = dn.tolist()
        counts = counts.tolist()
        v = 0.
        for d, p in zip(dn, counts):
            v += d * np.log2(p)
        entropy.append(-v)
    return entropy

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
        num = 4. * get_covariance(x, y) * meanx * meany
        denom = (varx + vary) * (meanx ** 2 + meany ** 2)
        val = num/denom
        qi.append(val)
    return qi

def write_list_to_file(l, fp, text = ""):
    for (index, val) in enumerate(l):
        fp.write(text + " Band # " + str(index + 1) + " = " + str(val) + "\n")
    fp.write("\n")

def get_psnr(rmse):
    psnr = []
    R = 2 ** 16 - 1
    for r in rmse:
        psnr.append(20. * np.log10(R / r))
    return psnr

def do_analysis(multispec, image, itr):
    print("ANALYSIS FOR IMAGE #" + str(itr) + " STARTED...")
    fp = open("Outputs/Analysis_" + str(itr) + ".txt", "w")
    fp.write("IMAGE = " + image.GetDescription() + "\n\n")
    qi = image_quality_index(multispec, image)
    write_list_to_file(qi, fp, "IMAGE QUALITY")
    rmse = get_rmse(multispec, image)
    write_list_to_file(rmse, fp, "RMSE")
    psnr = get_psnr(rmse)
    write_list_to_file(psnr, fp, "PSNR")
    diff, norm = get_relative_mean(multispec, image)
    fp.write("Relative mean = " + str(norm) + "\n\n")
    write_list_to_file(diff.tolist(), fp, "RELATIVE MEAN")
    entropy = get_entropy(image)
    write_list_to_file(entropy, fp, "ENTROPY")
    corrcoefs = get_corrcoef(multispec, image)
    fp.write("Corrcoef between " + multispec.GetDescription() + " and " + image.GetDescription() + "\n")
    write_list_to_file(corrcoefs, fp)
    for img in images:
        if image != img:
            fp.write("Corrcoef between " + image.GetDescription() + " and " + img.GetDescription() + "\n")
            corrcoefs = get_corrcoef(image, img)
            write_list_to_file(corrcoefs, fp)
    fp.close()
    print("ANALYSIS FOR IMAGE #" + str(itr) + " COMPLETE!")

multispec = read_image(r"D:/M8/Fusion_prac_data/optical_fusion_data/xs_subiko.img")
pcfused = read_image(r"D:/M8/Fusion_prac_data/Fused_New/pcfused.img")
broveyfused = read_image(r"D:/M8/Fusion_prac_data/Fused_New/broveyfused.img")
mulfused = read_image(r"D:/M8/Fusion_prac_data/Fused_New/mulfused.img")
hpffused = read_image(r"D:/M8/Fusion_prac_data/fused/hpffused.img")
ihsfused = read_image(r"D:/M8/Fusion_prac_data/fused/ihsfused.img")
ehlrsfused = read_image(r"D:/M8/Fusion_prac_data/Fused_New/ehlrsfused.img")
waveletfused = read_image(r"D:/M8/Fusion_prac_data/fused/waveletfused.img")
images = [pcfused, broveyfused, mulfused, hpffused, ihsfused, ehlrsfused, waveletfused]

threads = []
if not os.path.exists("Outputs"):
    os.makedirs("Outputs")
for (index, image) in enumerate(images):
    t = Thread(target = do_analysis, args = (multispec, image, index + 1))
    threads.append(t)
    t.start()
for t in threads:
    t.join()
print("\n\nANALYSIS COMPLETED!")