from quantumimageencoding.FRQI import FRQI
from quantumimageencoding.QPIE import QPIE
from utils import showdiff
from PIL import Image

Encoder = FRQI()
#try binary image
# image1 = Encoder.preProcessImage(Image.open('./testimages/test4edges.png').convert('L'))
arr = [ [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 0, 0, 0, 0, 0],
        [0, 1, 1, 0, 0, 0, 0, 0],
        [0, 1, 1, 0, 0, 0, 0, 0],
        [0, 1, 1, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0]]

image1 = arr
Encoder.encode(image1)
image2 = Encoder.decode('aer_simulator', shots=2**24)
# image2 = Encoder.detectEdges()
showdiff(Encoder, image1, image2)