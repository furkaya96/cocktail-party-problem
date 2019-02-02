import numpy as np
import soundfile as sf
import argparse as ap
import preprocess_sound as ps
import FastICA as fastica


def find_pair_of_mixed_file(mixed_file_number):
	if mixed_file_number % 2 == 0:
		mixed_data1, sample_rate1 = sf.read('./sounds/mixed/mixed' + str(mixed_file_number) + '.flac')
		mixed_data2, sample_rate2 = sf.read('./sounds/mixed/mixed' + str(mixed_file_number + 1) + '.flac')
	else:
		mixed_data1, sample_rate1 = sf.read('./sounds/mixed/mixed' + str(mixed_file_number - 1) + '.flac')
		mixed_data2, sample_rate2 = sf.read('./sounds/mixed/mixed' + str(mixed_file_number) + '.flac')
	return mixed_data1, mixed_data2, sample_rate1, sample_rate2


def get_independent_components(whitened_data):
	weights = []
	for i in range(whitened_data.shape[0]):
		weight = fastica.FastICA(whitened_data, weights)
		weights.append(weight)
	weights = np.vstack(weights)
	independent_components = np.dot(weights, whitened_data)
	return independent_components


def save_separated_sounds(independent_components, sample_rate, file_number):
	if file_number % 2 == 0:
		sf.write('./sounds/separated/separated' + str(file_number) + '.flac', independent_components[0], sample_rate)
		sf.write('./sounds/separated/separated' + str(file_number + 1) + '.flac', independent_components[1], sample_rate)
	else:
		sf.write('./sounds/separated/separated' + str(file_number - 1) + '.flac', independent_components[0], sample_rate)
		sf.write('./sounds/separated/separated' + str(file_number) + '.flac', independent_components[1], sample_rate)


# initialize argument parser object
parser = ap.ArgumentParser()
# read the arguments
parser.add_argument('--mixed_file', '-mf', type=int, help='select the mixed file you want the sounds to be separated from. e.g.: 12')
# hold arguments in args
args = vars(parser.parse_args())
# file number for finding mixed pair
mixed_file_number = args['mixed_file']
# find pair of mixed file
mixed_data1, mixed_data2, sample_rate1, sample_rate2 = find_pair_of_mixed_file(mixed_file_number)
# centering process
centered_mixed1 = ps.centering_process(mixed_data1)
centered_mixed2 = ps.centering_process(mixed_data2)
# mixed datas vertical stack
mixed_data_stack = np.vstack((centered_mixed1, centered_mixed2))
# whitening process
whitened_data = ps.whitening_process(mixed_data_stack)
# get separated independent components
independent_components = get_independent_components(whitened_data)
save_separated_sounds(independent_components, sample_rate1, mixed_file_number)
