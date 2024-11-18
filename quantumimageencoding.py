from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit.circuit.library.standard_gates import RYGate
from skimage.metrics import mean_squared_error, structural_similarity
from qiskit import execute, Aer
from PIL import Image
import numpy

class QuantumEncoder:
    def __init__(self):
        self.Qregs : QuantumRegister = None
        self.Cregs : ClassicalRegister = None
        self.Qcirc : QuantumCircuit = None

    def createQuantumCircuit(self, *regs) -> None :
        self.Qcirc = QuantumCircuit(*regs)

    def encode(self, image : Image.Image) -> None :
        pass

    def decode(self, circuit : QuantumCircuit) -> None:
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

class FRQI(QuantumEncoder):
    def __init__(self):
        pass
    
    def preProcessImage(self, image : Image.Image) -> Image.Image :
        '''
            This function makes sure that an image is in the form of 2^nx2^n.
            This is done since FRQI manages images of these size since it requires
            correct number of qubits.
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
        '''
            This function encodes the corresponding angle values of each element
            onto the Quantum Circuit.
        '''
        angles = numpy.arcsin(numpy.array(image) / 255)
        angles = angles.reshape(angles.shape[0]**2)

        controlbits = int(numpy.log2(angles.shape[0]))
        positions = QuantumRegister(controlbits, 'position')
        target = QuantumRegister(1, 'target')
        classical = ClassicalRegister(controlbits+1, 'measure')
        self.createQuantumCircuit(positions, target, classical)

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

    def decode(self, simulator : str, shots: int = 2**16):
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
        retrieved_image = retrieved_image.astype(numpy.uint8)
        retrieved_image = retrieved_image.reshape((picture_side, picture_side))
        return Image.fromarray(retrieved_image)

class NEQR(QuantumEncoder):
    def __init__(self):
        pass
    
    # def encode_image_neqr(self, image):
    #     # Convert the image to a NumPy array
    #     img_np = np.array(image)

    #     # Calculate the qubit dimension
    #     n = int(np.log2(img_np.shape[0]))
    #     qubit = 2 * n + 8
        
    #     # Calculate the number of bits needed for position encoding
    #     for_two = len(bin(img_np.shape[0]**2-1)) - 2
        
    #     # Initialize a zero-filled array of complex numbers with size 2**qubit
    #     encoded_state = np.zeros(2**qubit, dtype=complex)

    #     # Fill the array and set corresponding elements to 1
    #     for x_idx in range(img_np.shape[0]):
    #         for y_idx in range(img_np.shape[1]):
    #             pixel_val = img_np[x_idx, y_idx]
    #             position = y_idx * img_np.shape[1] + x_idx
    #             encoded_state[combine_values(pixel_val, position, for_two)] = 1

    #     # Normalize the array
    #     encoded_state /= np.linalg.norm(encoded_state)

    #     return encoded_state

    # def combine_values(pixel_val, position, n):
    #     # Convert pixel_val to a binary string
    #     pixel_binary = format(pixel_val, '08b')
    #     # Convert position to a binary string of a given length n
    #     position_binary = format(position, '0' + str(n) + 'b')
    #     # Concatenate binary strings
    #     combined_binary = pixel_binary + position_binary
    #     # Convert the concatenated binary string to a decimal number
    #     combined_decimal = int(combined_binary, 2)
    #     return combined_decimal

    # def decode_neqr(encoded_image):
    #     # Calculate the dimension of the image
    #     image_size = int(len(encoded_image) // 256)
    #     x_lim = int(np.sqrt(image_size))
        
    #     # Create an array for the decoded image
    #     decoded_image = np.zeros((image_size), dtype=int)

    #     # Extract nonzero indices and their values
    #     nonzero_indices = np.nonzero(encoded_image)[0]
    #     n = len(bin(len(encoded_image)-1))-2
        
    #     # Decode and fill the image
    #     for i in nonzero_indices:
    #         position_binary = format(i, '0' + str(n) + 'b')
    #         pixel_val = position_binary[:8]  
    #         pixel_position = position_binary[8:]  
    #         pixel_val_decimal = int(pixel_val, 2)  
    #         pixel_position_decimal = int(pixel_position, 2)  
    #         decoded_image[pixel_position_decimal] = pixel_val_decimal

    #     # Reshape the decoded image to its original dimensions
    #     return decoded_image.reshape((x_lim, x_lim), order='F')