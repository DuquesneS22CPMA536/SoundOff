from scipy.io import wavfile as w # using this library instead; was having issues with wav library to actually save the data from the wav file

class WavFile:
    '''The wav file and its measurements.
    
    Will open the wav file and calculate its peak and LUFS values.
    
    Attributes:
        sample_rate: Integer sample rate from the wav file
        data: Numpy array data from the wav file
        length_file: Integer length of self.data
        nchannels: Integer number of channels from the wav file
    '''
    def __init__(self, filename):
        '''Opens the wav file and fetches its needed information.
        
        Will open the wav file and fetch its sample rate, data itself, length of data, and number of channels.
        
        Args:
            self: A WavFile Object.
            filename: String from App object which is the selected wav file.
        
        Raises:
            Add possible errors here.
        
        '''
        # Reading in the wav file, filename, and getting its sample rate, data, length of the file, and number of channels
        [self.sample_rate, self.data] = w.read(filename)
        self.length_file = len(self.data)
        if len(self.data.shape) > 1: # if the wav file has more than 1 channel; otherwise it has 1 channel
            self.nchannels = self.data.shape[1]
        else:
            self.nchannels = 1

    # Getting the peak of the wav file
    def get_peak_std(self):
        '''Fetches its peak value.
        
        Will calculate and return the peak loudness value.
        
        Args:
            self: A WavFile Object.
        
        Returns:
            An integer containing the peak loudness value.
        
        Raises:
            Add possible errors here.
        
        '''
        if self.nchannels == 1:
            return max(self.data)
        else:
            channel_maxes = []
            for i in range(0,self.nchannels):
                channel_maxes.append(max(self.data[:,i]))
            return max(channel_maxes)