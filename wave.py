from scipy.io import wavfile # using this library instead; was having issues with wav library to actually save the data from the wav file

class WavFile:
    def __init__(self, filename): # filename would be App.filename
        # Reading in the wav file, filename, and getting its sample rate, data, length of the file, and number of channels
        [self.sample_rate, self.data] = wavfile.read(filename)
        self.length_file = len(self.data)
        self.nchannels = self.data.shape[1]

    # Getting the peak of the wav file
    def get_peak_std(self):
        return max(self.data)
