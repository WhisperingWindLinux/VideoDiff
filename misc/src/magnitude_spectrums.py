import cv2
import numpy as np
import matplotlib.pyplot as plt

image = cv2.imread('file_path')
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

channels = cv2.split(image_rgb)

dft_channels = [cv2.dft(np.float32(channel), flags=cv2.DFT_COMPLEX_OUTPUT) for channel in channels]
dft_shift_channels = [np.fft.fftshift(dft) for dft in dft_channels]

magnitude_spectrums = [20 * np.log(cv2.magnitude(dft_shift[:, :, 0], dft_shift[:, :, 1])) for dft_shift in dft_shift_channels]

plt.figure(figsize=(18, 6))
plt.subplot(141), plt.imshow(image_rgb)
plt.title('Source image'), plt.xticks([]), plt.yticks([])
for i, magnitude_spectrum in enumerate(magnitude_spectrums):
    plt.subplot(142 + i), plt.imshow(magnitude_spectrum, cmap='gray')
    plt.title(f'Magnitude spectrums (Channel {i})'), plt.xticks([]), plt.yticks([])
plt.show()