import numpy as np


def bring_equal_length(data1, data2):
    """ Brings the audio data of two different
    lengths between the two to the minimum length.

    For example sound1 is 23 second, sound2 is 30 second.
    This function returns both sounds 23 seconds long
    (minimum one).

    Args:
        data1 (numpy.ndarray): the first sound data.
        data2 (numpy.ndarray): the second sound data.
    Returns:
        data1 (numpy.ndarray): the first data in the new length.
        data2 (numpy.ndarray): the second data in the new length.
    """
    min_length = min(data1.shape[0], data2.shape[0])
    data1 = data1[0:min_length]
    data2 = data2[0:min_length]
    return data1, data2


def centering_process(data):
    """ The centering matrix is a symmetric and idempotent matrix,
    which when multiplied with a vector has the same effect as
    subtracting the mean of the components of the vector from every component.

    Args:
        data          (numpy.ndarray): the mixed sound data.
    Returns:
        centered_data (numpy.ndarray): the centered mixed sound data.
    """
    centered_data = data - np.mean(data)
    return centered_data


def whitening_process(mixed_signal_matrix):
    """ Whitening is an operation that removes all linear dependencies in a data set
    and normalizes the variance along all dimensions.

    Args:
        mixed_signal_matrix (numpy.ndarray): non whitened matrix which includes mixed sound datas.
    Returns:
        whitened_matrix     (numpy.ndarray): the matrix that linear dependencies deleted matrix.
    """
    covariance_matrix = np.cov(mixed_signal_matrix)
    eigen_value, eigen_vector = np.linalg.eigh(covariance_matrix)
    diagonal_matrix = np.diag(eigen_value)
    invert_square_root = np.sqrt(np.linalg.pinv(diagonal_matrix))
    whiten_transformation = np.dot(eigen_vector, np.dot(invert_square_root, np.transpose(eigen_vector)))
    whitened_matrix = np.dot(whiten_transformation, mixed_signal_matrix)
    return whitened_matrix
