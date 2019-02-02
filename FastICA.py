import numpy as np


def sigmoid(z):
	return 1. / (1. + np.exp(-z))


def sigmoid_derivative(z):
	return sigmoid(z) * (1. - sigmoid(z))


def FastICA(mixed_signal_matrix, weights):
	""" FastICA seeks an orthogonal rotation of prewhitened data, through
	a fixed-point iteration scheme, that maximizes a measure of non-gaussianity
	of the rotated components.

	Args:
	    mixed_signal_matrix (numpy.ndarray): the matrix of mixed sound datas.
	    weights						 (list): the weight list.
	Returns:
	    weight1 			(numpy.ndarray): final weight of the signal.
	"""
	num_of_signal = mixed_signal_matrix.shape[1]
	# initalize random unit vector.
	weight1 = np.random.rand(2)
	weight2 = np.random.rand(2)
	weight1 = np.divide(weight1, np.linalg.norm(weight1))
	weight2 = np.divide(weight2, np.linalg.norm(weight2))
	# if converged, return last updated weight vector.
	while np.abs(np.dot(np.transpose(weight1), weight2)) < 1:
		partition1 = np.dot(mixed_signal_matrix, sigmoid(np.dot(np.transpose(weight2), mixed_signal_matrix)))
		partition2 = np.mean(sigmoid_derivative(np.dot(np.transpose(weight2), mixed_signal_matrix))) * weight2
		weight1 = weight2
		weight2 = (partition1 / num_of_signal) - partition2
		weight3 = weight2
		for weight in weights:
			weight3 = weight3 - np.dot(np.transpose(weight2), weight) * weight
		weight2 = weight3
		weight2 = weight2 / np.linalg.norm(weight2)
	return weight1
