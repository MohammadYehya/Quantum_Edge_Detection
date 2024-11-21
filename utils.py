from matplotlib import pyplot as plt
from quantumimageencoding.BaseQuantumEncoder import QuantumEncoder
from PIL import Image

def showdiff(Encoder : QuantumEncoder, image1 : Image.Image, image2 : Image.Image):
    print('MSE: ',Encoder.calculateMSE(image1, image2))
    try:
        print('SSI: ', Encoder.calculateSSI(image1, image2))
    except:
        pass
    fig = plt.figure()
    fig.add_subplot(2,1,1)
    plt.imshow(image1, cmap='gray')
    fig.add_subplot(2,1,2)
    plt.imshow(image2, cmap='gray')
    plt.show()