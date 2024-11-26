from qiskit import QuantumRegister, ClassicalRegister
from qiskit.circuit.library.standard_gates import RYGate
from quantumimageencoding.BaseQuantumEncoder import QuantumEncoder
from qiskit import execute, Aer
from PIL import Image
import numpy

class FRQI(QuantumEncoder):
    def __init__(self):
        pass

    def encode(self, image : Image.Image) -> None :
        '''
            This function encodes the corresponding angle values of each element
            onto the Quantum Circuit.
        '''
        # angles = numpy.arcsin(numpy.array(image) / 255)
        angles = numpy.arcsin(numpy.array(image))   #To deal with binary images
        angles = angles.reshape(angles.shape[0]**2)

        controlbits = int(numpy.log2(angles.shape[0]))
        positions = QuantumRegister(controlbits, 'position')
        target = QuantumRegister(1, 'target')
        classical = ClassicalRegister(controlbits+1, 'measure')
        self.Qcirc = self.createQuantumCircuit(positions, target, classical)

        #FRQI process starts here
        for i in range(controlbits):
            self.Qcirc.h(i)
        j = 0
        for i in angles:
            state = '{0:0{1}b}'.format(j - 1, controlbits)
            new_state = '{0:0{1}b}'.format(j, controlbits)
            if j != 0:
                c = numpy.array([])
                for k in range(controlbits):
                    if state[k] != new_state[k]:
                        c = numpy.append(c, int(k))
                if len(c) > 0:
                    self.Qcirc.x(numpy.abs(c.astype(int) - (controlbits - 1)))
            cry = RYGate(2 * i).control(controlbits)
            aux = numpy.append([i for i in range(controlbits)], controlbits).tolist()
            self.Qcirc.append(cry, aux)
            j += 1

    def decode(self, simulator : str, shots: int = 2**16) -> Image.Image:
        n = [i for i in range(self.Qcirc.num_qubits)]
        self.Qcirc.measure(n, n)
        backend_sim = Aer.get_backend(simulator)
        
        job = execute(self.Qcirc, backend_sim, shots=shots)
        result = job.result()
        counts = result.get_counts(self.Qcirc)

        pixels = 2 ** (self.Qcirc.num_qubits - 1)
        picture_side = int(numpy.sqrt(pixels))
        binary_length = self.Qcirc.num_qubits - 1

        shots = counts.shots()
        
        retrieved_image = numpy.array([])
        for i in range(pixels):
            try:
                s = format(i, '0{0}b'.format(binary_length))
                new_s = '1' + s
                retrieved_image = numpy.append(retrieved_image, numpy.sqrt(counts[new_s] / shots))
            except KeyError:
                retrieved_image = numpy.append(retrieved_image, [0.0])
    
        retrieved_image = numpy.real(retrieved_image)
        retrieved_image *= picture_side * 255.0
        retrieved_image = numpy.floor((retrieved_image/100))    #To deal with binary images
        retrieved_image = retrieved_image.astype(numpy.uint8)
        retrieved_image = retrieved_image.reshape((picture_side, picture_side))
        return Image.fromarray(retrieved_image)
    
    def detectEdges(self, image : Image.Image):
        pass