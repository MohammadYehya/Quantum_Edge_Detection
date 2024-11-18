from qiskit import QuantumRegister, ClassicalRegister
from qiskit.circuit.library.standard_gates import RYGate
from quantumimageencoding.BaseQuantumEncoder import QuantumEncoder
from qiskit import execute, Aer
from PIL import Image
import numpy

class QPIE(QuantumEncoder):
    def __init__(self):
        pass
    
    def encode(self, image : Image.Image):
        pass