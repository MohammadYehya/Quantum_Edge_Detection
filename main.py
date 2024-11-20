from matplotlib import pyplot as plt
from quantumimageencoding.FRQI import FRQI
from quantumimageencoding.QPIE import QPIE
from utils import showdiff
from PIL import Image

Encoder = QPIE()
image1 = Encoder.preProcessImage(Image.open('./testimages/test4edges.png').convert('L'))
Encoder.encode(image1)
image2 = Encoder.detectEdges()
showdiff(Encoder, image1, image2)