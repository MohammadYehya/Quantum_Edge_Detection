from qiskit import QuantumCircuit
from qiskit.circuit.library.standard_gates import RYGate
from quantumimageencoding.BaseQuantumEncoder import QuantumEncoder
from qiskit import execute, Aer
from PIL import Image
import numpy

class QPIE(QuantumEncoder):
    def __init__(self):
        pass

    def amplitudeEncoder(self, img : numpy.ndarray) :
        img = img.astype(numpy.float64)
        rms = numpy.sqrt(numpy.sum(numpy.sum(img**2, axis=1)))
        amplitudes = (img/rms).reshape(img.shape[0]**2)
        # print(amplitudes)
        # print(numpy.sum(amplitudes**2))
        return amplitudes

    def encode(self, image : Image.Image) -> None :
        img = numpy.array(image)
        h_amplitudes = self.amplitudeEncoder(img)
        v_amplitudes = self.amplitudeEncoder(img.T)

        controlbits = int(2 * numpy.log2(img.shape[0]))
        unitaryMatrix = numpy.identity(2**(controlbits+1))
        unitaryMatrix = numpy.roll(unitaryMatrix,1,axis=1)

        # positions = QuantumRegister(controlbits, 'position')
        # target = QuantumRegister(1, 'target')
        # classical = ClassicalRegister(controlbits+1, 'measure')


        # self.Qcirc = self.createQuantumCircuit(positions, target, classical)
        self.Qcirc = QuantumCircuit(controlbits+1)
        self.Qcirc.initialize(h_amplitudes, range(1, controlbits+1))
        self.Qcirc.h(0)
        self.Qcirc.unitary(unitaryMatrix, range(controlbits+1))
        self.Qcirc.h(0)

        # self.Qcirc2 = self.createQuantumCircuit(positions, target, classical)
        self.Qcirc2 = QuantumCircuit(controlbits+1)
        self.Qcirc2.initialize(v_amplitudes, range(1, controlbits+1))
        self.Qcirc2.h(0)
        self.Qcirc2.unitary(unitaryMatrix, range(controlbits+1))
        self.Qcirc2.h(0)

        return self.Qcirc

    def decode(self, simulator : str, shots: int = 2**16) -> Image.Image :
        pass

    def detectEdges(self) -> Image.Image:
        back = Aer.get_backend('statevector_simulator')
        # self.Qcirc2.draw('mpl', fold=-1)
        results = execute([self.Qcirc, self.Qcirc2], backend=back).result()
        state_vector_h = results.get_statevector(self.Qcirc)
        state_vector_v = results.get_statevector(self.Qcirc2)

        size = int(2**((self.Qcirc.num_qubits-1)/2))
        threshold = lambda amp: (amp > 1e-15 or amp < -1e-15)
        h_edge_scan_img = numpy.abs(numpy.array([1 if threshold(state_vector_h[(2*i)+1].real) else 0 for i in range(2**(self.Qcirc.num_qubits-1))])).reshape(size, size)
        v_edge_scan_img = numpy.abs(numpy.array([1 if threshold(state_vector_v[(2*i)+1].real) else 0 for i in range(2**(self.Qcirc2.num_qubits-1))])).reshape(size, size).T

        edge_scan_image = h_edge_scan_img | v_edge_scan_img
        return edge_scan_image, h_edge_scan_img, v_edge_scan_img