def mix_sounds(data1, data2, weight1, weight2):
    """ Mixes the two given sound data at the given mixing ratios.
    Creates a mixed audio file similar to the relationship of the
    sound sources in the cocktail party problem to the microphones.

    For example the first sound source is 0.8 meters from the microphone,
    the second sound file is 0.2 meters from the microphone. The mixed
    sound file output from the function combine sounds at this rate.
    The sound that is so distant is a noise for this microphone.

    Args:
        data1 (numpy.ndarray): the first sound data.
        data2 (numpy.ndarray): the second sound data.
        weight1       (float): the weight of the first sound data.
        weight2       (float): the weight of the second sound data.
    Returns:
        mixed_sound (numpy.ndarray): the mix sound data.
    """
    mixed_sound = data1 * weight1 + data2 * weight2
    return mixed_sound
