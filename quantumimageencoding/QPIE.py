from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit.circuit.library.standard_gates import RYGate
from quantumimageencoding.BaseQuantumEncoder import QuantumEncoder
from qiskit import execute, Aer
from PIL import Image
import numpy

class QPIE(QuantumEncoder):
    def __init__(self):
        self.Qcirc2 : QuantumCircuit = None
    
    def amplitudeEncoder(self, img : numpy.ndarray) -> Image.Image :
        rms = numpy.sqrt(numpy.sum(numpy.sum(img**2, axis=1)))
        amplitudes = (img/rms).reshape(img.shape[0]**2)
        return amplitudes
    
    def encode(self, image : Image.Image) -> None :
        img = numpy.array(image)
        h_amplitudes = self.amplitudeEncoder(img)
        v_amplitudes = self.amplitudeEncoder(img.T)

        controlbits = int(2 * numpy.log2(img.shape[0]))
        unitaryMatrix = numpy.identity(2**(controlbits+1))
        unitaryMatrix = numpy.roll(unitaryMatrix,1,axis=1)

        positions = QuantumRegister(controlbits, 'position')
        target = QuantumRegister(1, 'target')
        classical = ClassicalRegister(controlbits+1, 'measure')

        self.Qcirc = self.createQuantumCircuit(positions, target, classical)
        self.Qcirc.initialize(h_amplitudes, range(controlbits))
        self.Qcirc.h(controlbits)
        self.Qcirc.unitary(unitaryMatrix, range(controlbits+1))
        self.Qcirc.h(controlbits)
        
        self.Qcirc2 = self.createQuantumCircuit(positions, target, classical)
        self.Qcirc2.initialize(v_amplitudes, range(controlbits))
        self.Qcirc2.h(controlbits)
        self.Qcirc2.unitary(unitaryMatrix, range(controlbits+1))
        self.Qcirc2.h(controlbits)


    def decode(self, simulator : str, shots: int = 2**16) -> Image.Image :
        pass

    def detectEdges(self):
        backend_sim = Aer.get_backend('statevector_simulator')
        results = execute([self.Qcirc, self.Qcirc2], backend=backend_sim).result()
        state_vector_h = results.get_statevector(self.Qcirc)
        state_vector_v = results.get_statevector(self.Qcirc2)

        threshold = lambda amp: (amp > 1e-15 or amp < -1e-15)
        h_edge_scan_img = numpy.abs(numpy.array([1 if threshold(state_vector_h[(2*i)+1].real) else 0 for i in range(2**(self.Qcirc.num_qubits-1))])).reshape(8, 8)
        v_edge_scan_img= numpy.abs(numpy.array([1 if threshold(state_vector_v[(2*i)+1].real) else 0 for i in range(2**(self.Qcirc2.num_qubits-1))])).reshape(8, 8).T

        edge_scan_image = h_edge_scan_img | v_edge_scan_img
        print(edge_scan_image)