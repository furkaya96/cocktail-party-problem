import soundfile as sf
import argparse as ap
import glob
import mix_sound as ms
import preprocess_sound as ps


def create_mixed_sounds(category1, category2, mix_rate):
    """ Performs a blending between the entered audio categories.
    It finds the folder of the given categories in the data set and combines all
    the sounds at the mutually given rate. If two categories are entered the same,
    it makes a blend in itself.

    For example, when the speech and noise categories are entered, they find the
    "speech" and "noise" folders in the sounds folder and mix all the .flac
    extension files. A total of 25 0.8 weight speech and 0.2 weight noise,
    25 weight 0.2 speech and 0.8 weight noise make a mixed sound.

    Args:
        category1 (str): first sound category to be used in mixing.
        category2 (str): second sound category to be used in mixing.
        mix_rate  (int): mixing ratio.
    """
    file_num_category1 = len(glob.glob1('./sounds/' + category1 + '/', "*.flac"))
    file_num_category2 = len(glob.glob1('./sounds/' + category2 + '/', "*.flac"))
    # returns the total number of audio files in the mixed folder to prevent overwrite!
    mix_count = len(glob.glob1('./sounds/mixed/', "*.flac"))
    if category1 != category2:
        for i in range(file_num_category1):
            category1_file, sample_rate1 = sf.read('./sounds/' + category1 + '/' + category1 + str(i) + '.flac')
            for j in range(file_num_category2):
                category2_file, sample_rate2 = sf.read('./sounds/' + category2 + '/' + category2 + str(j) + '.flac')
                category1_file, category2_file = ps.bring_equal_length(category1_file, category2_file)
                mix1 = ms.mix_sounds(category1_file, category2_file, mix_rate, 1 - mix_rate)
                mix2 = ms.mix_sounds(category2_file, category1_file, mix_rate, 1 - mix_rate)
                sf.write('./sounds/mixed/mixed' + str(mix_count) + '.flac', mix1, sample_rate1)
                sf.write('./sounds/mixed/mixed' + str(mix_count + 1) + '.flac', mix2, sample_rate1)
                mix_count += 2
    else:
        for i in range(file_num_category1):
            category1_file, sample_rate1 = sf.read('./sounds/' + category1 + '/' + category1 + str(i) + '.flac')
            for j in range(file_num_category2):
                # to prevent the audio file from mixing with itself!
                if i < j:
                    category2_file, sample_rate2 = sf.read('./sounds/' + category2 + '/' + category2 + str(j) + '.flac')
                    category1_file, category2_file = ps.bring_equal_length(category1_file, category2_file)
                    mix1 = ms.mix_sounds(category1_file, category2_file, mix_rate, 1 - mix_rate)
                    mix2 = ms.mix_sounds(category2_file, category1_file, mix_rate, 1 - mix_rate)
                    sf.write('./sounds/mixed/mixed' + str(mix_count) + '.flac', mix1, sample_rate1)
                    sf.write('./sounds/mixed/mixed' + str(mix_count + 1) + '.flac', mix2, sample_rate2)
                    mix_count += 2


# initialize argument parser object
parser = ap.ArgumentParser()
# read the arguments
parser.add_argument('--first_category', '-c1', help='first category that mix with sounds of second category')
parser.add_argument('--second_category', '-c2', help='second category that mix with sounds of first category')
parser.add_argument('--mix_rate', '-mr', type=float, default=0.7, help='mix rate should be (0.6, 0.9)')
# hold arguments in args
args = vars(parser.parse_args())
create_mixed_sounds(args['first_category'], args['second_category'], args['mix_rate'])
