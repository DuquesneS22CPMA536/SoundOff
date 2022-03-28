from wave import WavFile as w

def test_wavFileOpen():
    wavFile = w('StarWars3.wav')
    assert 22050 == wavFile.sample_rate
    assert 66150 == wavFile.length_file
    assert 1 == wavFile.nchannels

def test_wavFileMultChannels():
    wavFile = w('piano2.wav')
    assert 48000 == wavFile.sample_rate
    assert 302712 == wavFile.length_file
    assert 2 == wavFile.nchannels