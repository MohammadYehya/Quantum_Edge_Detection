import numpy
from skimage.transform import resize

def Sobel(img, size):
    img = resize(img, (size, size), order=1, preserve_range=True, anti_aliasing=False).astype(numpy.uint8)
    Gx = numpy.array([[-1, 0, 1],
                      [-2, 0, 2],
                      [-1, 0, 1]])
    Gy = numpy.array([[-1, -2, -1],
                      [ 0,  0,  0],
                      [ 1,  2,  1]])

    rows, cols = img.shape
    gradient_x = numpy.zeros_like(img, dtype=float)
    gradient_y = numpy.zeros_like(img, dtype=float)
    gradient_magnitude = numpy.zeros_like(img, dtype=float)

    for i in range(1, rows - 1):
        for j in range(1, cols - 1):
            region = img[i-1:i+2, j-1:j+2]
            gradient_x[i, j] = numpy.sum(region * Gx)
            gradient_y[i, j] = numpy.sum(region * Gy)

    gradient_magnitude = numpy.sqrt(gradient_x**2 + gradient_y**2)
    gradient_magnitude = (gradient_magnitude / gradient_magnitude.max()) * 255
    edges = (gradient_magnitude > 200).astype(numpy.uint8)
    return edges