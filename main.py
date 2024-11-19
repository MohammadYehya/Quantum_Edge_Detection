from quantumimageencoding.FRQI import FRQI
from quantumimageencoding.QPIE import QPIE
from utils import showdiff
from PIL import Image

Encoder = QPIE()
image1 = Encoder.preProcessImage(Image.open('./testimages/test4.png').convert('L'))
Encoder.encode(image1)
Encoder.detectEdges()
# image2 = Encoder.decode('aer_simulator', shots=2**24)

# showdiff(Encoder, image1, image2)