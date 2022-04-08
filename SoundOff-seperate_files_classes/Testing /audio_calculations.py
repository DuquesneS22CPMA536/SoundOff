import soundfile as sf
import pyloudnorm as pyln
import numpy as np
import scipy
import math
import resampy
import statistics
import moviepy.editor as mp

class audio_calculations():
    """Opening file and calculations for LUF and True Peak.

    Will open a wav or mp4 file, test its peak value against
    a standard's peak value, and test its LUF value against a standard's LUF value.

    Attributes:
        file_path: The current audio file path to be tested. Can change frequently. String object.
    """

    def __init__(self, file_path):
        """Initializes the file to be tested.

        Will store the file to be tested.

        Args:
          self: The main object
          file_path: String containing the name of the file

        Raises:
          Any errors raised should be put here

        """
        # initialize path of the file being passed in
        self.file_path = file_path

    def get_file_path(self):
        """ Gives the current file name being stored by the object

        Returns the filename attribute being stored.

        Args:
            self: Instance of main object

        Returns:
            file_path: the file path of the audio file selected by the user

        Raises:
            Any errors raised should be put here

        """
        return self.file_path

    def open_wav_file(self):
        """Opens the wav file and fetches its needed information.

        Opens the selected wav file and fetches its sample rate, data itself, length of data, and number of channels.

        Args:
            self: A main Object.

        Returns:
            A tuple containing the selected wav file's sample rate, data, length of data, and number of channels.

        Raises:
            Add possible errors here.

        """
        fileType = self.get_file_path().split('.') #split file path on '.'
        fileType = fileType[-1] #take the last entry in the list from split as the file extension

        #if the file is an MP4 file then open using moviepy and extract the audio
        if fileType.upper() == 'MP4':
            clip = mp.VideoFileClip(self.get_file_path())
            audioFile = clip.audio
            data = audioFile.to_soundarray(None,44100)
            rate = 44100
        else: #else open as an audio (wav/flac) file
            data, rate = sf.read(self.get_file_path())

        length_file = len(data)

        if len(data.shape) > 1:
            n_channels = data.shape[1]
        else:
            n_channels = 1

        wav_info = (data, rate, length_file, n_channels)

        return wav_info

    def get_luf(self, wav_info):
        """Returns the integrated loudness in LUFS of an audio file.

        Uses pyloudnorm to find the LUFS of an audio file found at a file path passed.

        Args:
            self: Instance of main object
            wav_info: a tuple of the selected wav file's sample rate, data, length of data, number of channels

        Returns:
            The integrated loudness of the audio file in LUFS

        Raises:
            Any errors raised should be put here

        """

        meter = pyln.Meter(wav_info[1])  # create meter; wav_info[1] is the rate
        lufs = meter.integrated_loudness(wav_info[0])  # get lufs value; wav_info[0] is the data
        return lufs

    def get_peak(self, wav_info):
        """Returns the true peak in dB of an audio file.

        Uses some method to find the peak of an audio file found at a file path passed.

        Args:
            self: Instance of main object
            wav_info: a tuple of the selected wav file's sample rate, data, length of data, number of channels

        Returns:
            The true peak of the audio file in dB

        Raises:
            Any errors raised should be put here

        """
        resampling_factor = 4  # use a resampling factor of 4

        # calculate number of samples in resampled file
        samples = wav_info[2] * resampling_factor  # wav_info[2] is the length of the data

        # resample using FFT
        new_audio = scipy.signal.resample(wav_info[0], samples)
        current_peak1 = np.max(np.abs(new_audio))  # find peak value
        current_peak1 = math.log(current_peak1, 10) * 20  # convert to decibels

        # resample using resampy
        new_audio = resampy.resample(wav_info[0], wav_info[2], samples, axis=-1)
        current_peak2 = np.max(np.abs(new_audio))  # find peak value
        current_peak2 = math.log(current_peak2, 10) * 20  # convert to decibels

        # resample using polynomial
        new_audio = scipy.signal.resample_poly(wav_info[0], resampling_factor, 1)
        current_peak3 = np.max(np.abs(new_audio))  # find peak value
        current_peak3 = math.log(current_peak3, 10) * 20  # convert to decibels

        # get and return median of the three techniques
        peak = statistics.median([current_peak1, current_peak2, current_peak3])
        return peak
