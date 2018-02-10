from matplotlib import pyplot as plt
from numpy import loadtxt

for i in range(1, 7):
	X = loadtxt('Grass_spectra/grass' + str(i))
	wavelength = X[:, 0]
	reflectance = X[:, 1]
	plt.plot(wavelength, reflectance, label='grass'+str(i))
plt.title('Grass Spectra')
plt.xlabel('Wavelength')
plt.ylabel('Reflectance')
plt.legend()
plt.show()
