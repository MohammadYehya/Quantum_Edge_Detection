from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from skimage.metrics import mean_squared_error, structural_similarity
from PIL import Image
import numpy

class QuantumEncoder:
    def __init__(self):
        self.Qregs : QuantumRegister = None
        self.Cregs : ClassicalRegister = None
        self.Qcirc : QuantumCircuit = None

    def createQuantumCircuit(self, *regs) -> None :
        return QuantumCircuit(*regs)

    def preProcessImage(self, image : Image.Image) -> Image.Image :
        '''
            This function makes sure that an image is in the form of 2^nx2^n.
            This is done since most encoders manage images of these size since
            it requires correct number of qubits.
        '''
        image = image.convert('L')  #Converting to Grayscale
        img = numpy.array(image)    #Converting image to a numpy array
        squareSize = max(2**int(numpy.ceil(numpy.log2(image.size[0]))), 2**int(numpy.ceil(numpy.log2(image.size[1]))))  #Calculating size of square to accomodate image
        new_img = numpy.zeros((squareSize,squareSize))  #Creating an array to store new image
        for i in range(image.size[1]):
            for j in range(image.size[0]):
                new_img[i, j] = img[i, j]
        return Image.fromarray(new_img)

    def encode(self, image : Image.Image) -> None :
        pass

    def decode(self, circuit : QuantumCircuit) -> None:
        pass

    def detectEdges(self, image:Image.Image):
        pass

    def calculateMSE(self, image1 : Image.Image, image2 : Image.Image):
        img1_array = numpy.array(image1)
        img2_array = numpy.array(image2)
        mse = mean_squared_error(img1_array, img2_array)
        return mse
        
    def calculateSSI(self, image1 : Image.Image, image2 : Image.Image):
        img1_array = numpy.array(image1)
        img2_array = numpy.array(image2)
        ssim = structural_similarity(img1_array, img2_array, multichannel=False, data_range=255)
        return ssim