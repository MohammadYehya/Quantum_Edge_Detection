from quantumimageencoding import FRQI, NEQR
from utils import showdiff
from PIL import Image

Encoder = NEQR()
image1 = Encoder.preProcessImage(Image.open('./testimages/test4.png').convert('L'))
# Encoder.encode(image1)
# image2 = Encoder.decode('aer_simulator', shots=2**24)

# showdiff(Encoder, image1, image2)