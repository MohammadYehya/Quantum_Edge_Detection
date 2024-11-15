from qiskit import IBMQ, QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit import execute, QuantumRegister
from qiskit.qasm import pi
from qiskit.tools.visualization import plot_histogram, circuit_drawer
from qiskit import execute, Aer, BasicAer
import numpy as np
# import random
# import keras
# from keras.models import Sequential
# from keras.layers import Dense, Activation
# from keras.datasets import mnist
import matplotlib.pyplot as plt
# from sklearn.metrics import mean_squared_error, mean_absolute_error, mutual_info_score, r2_score
# from qiskit.circuit.library.standard_gates import RYGate, RYYGate
# import cv2
import pandas as pd
from utils import frqi

# Read the csv file
dataset = pd.read_csv('mnist-resized.csv')
# Reshape and transform the dataframe into a numpy array
images = dataset.to_numpy()[:,1:].reshape(42000,8,8)
pixel_values = images.reshape(42000,64)
fig = plt.figure()
fig.add_subplot(2,1,1)
plt.imshow(images[0,:], cmap='gray')
normalized_pixels = pixel_values/255.0
angles = np.arcsin(normalized_pixels[0,:])

qr = QuantumRegister(7,'q')
cr = ClassicalRegister(7,'c')
qc = QuantumCircuit(qr,cr)

# Call the frqi function and add all the necessary parameters
frqi(qc, [0,1,2,3,4,5], 6, angles)
# qc.draw(output = 'mpl')

qc.measure([0,1,2,3,4,5,6],[0,1,2,3,4,5,6])

backend_sim = Aer.get_backend('qasm_simulator')
numOfShots = 1048576
result = execute(qc, backend_sim, shots=numOfShots).result()

# print(result.get_counts(qc))

# plot_histogram(result.get_counts(qc), figsize=(20,7))
retrieve_image = np.array([])

for i in range(64):
  try:
    s = format(i, '06b')
    new_s = '1' + s
    retrieve_image = np.append(retrieve_image,np.sqrt(result.get_counts(qc)[new_s]/numOfShots))
  except KeyError:
    retrieve_image = np.append(retrieve_image,[0.0])

retrieve_image *=  8.0*255.0
retrieve_image = retrieve_image.astype('int')
retrieve_image = retrieve_image.reshape((8,8))
fig.add_subplot(2,1,2)
plt.imshow(retrieve_image, cmap='gray', vmin=0, vmax=255)
plt.show()