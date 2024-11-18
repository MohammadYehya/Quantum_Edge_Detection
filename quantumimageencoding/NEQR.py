from qiskit import QuantumRegister, ClassicalRegister
from qiskit.circuit.library.standard_gates import RYGate
from quantumimageencoding.BaseQuantumEncoder import QuantumEncoder
from qiskit import execute, Aer
from PIL import Image
import numpy

class NEQR(QuantumEncoder):
    def __init__(self):
        pass
    
    def encode(self, image : Image.Image):
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