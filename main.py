from quantumimageencoding import *
from utils import showdiff

FRQIEncoder = FRQI()
image1 = FRQIEncoder.preProcessImage(Image.open('./testimages/test8.png').convert('L'))
FRQIEncoder.encode(image1)
image2 = FRQIEncoder.decode('aer_simulator', shots=2**24)

showdiff(FRQIEncoder, image1, image2)

