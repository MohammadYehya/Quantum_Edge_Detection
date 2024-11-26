from matplotlib import pyplot as plt
from quantumimageencoding.BaseQuantumEncoder import QuantumEncoder
from PIL import Image
def showdiff(Encoder : QuantumEncoder, *images : Image.Image):
    # print('MSE: ',Encoder.calculateMSE(image1, image2))
    # try:
    #     print('SSI: ', Encoder.calculateSSI(image1, image2))
    # except:
    #     pass
    fig = plt.figure()
    for i in range(len(images)):
        fig.add_subplot(1,len(images),i+1)
        plt.imshow(images[i], cmap='gray')
    plt.show()