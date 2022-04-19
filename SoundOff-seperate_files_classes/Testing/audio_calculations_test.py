from audio_calculations import audio_calculations as ac

#One Channel 24-bit Wave File
def test_One_24():
    a = ac('SineWave.wav')
    info = a.open_wav_file()
    assert 48000 == info[1]
    assert 480000 == info[2]
    assert 1 == info[3]

    peak = a.get_peak(info)
    assert -6.0 == round(peak,1)

    lufs = a.get_luf(info)
    assert -9.0 == round(lufs,1)
    
#One Channel 16-bit wave file
def test_One_16():
    a = ac('testfiles/BabyElephantWalk60.wav')
    info = a.open_wav_file()
    assert 22050 == info[1]
    assert 1323000 == info[2]
    assert 1 == info[3]

    peak = a.get_peak(info)
    assert -5.3 == round(peak,1)

    lufs = a.get_luf(info)
    assert -22.9 == round(lufs,1)
    
#One Channel 8-bit wave file
def test_One_8():
    a = ac('testfiles/taunt.wav')
    info = a.open_wav_file()
    assert 22257 == info[1]
    assert 91240 == info[2]
    assert 1 == info[3]

    peak = a.get_peak(info)
    assert -0.6 == round(peak,1)

    lufs = a.get_luf(info)
    assert -11.5 == round(lufs,1)

#Two Channel - 24-bit Flac file
def test_One_8():
    a = ac('2_Channel_24_48_minus6db.flac')
    info = a.open_wav_file()
    assert 48000 == info[1]
    assert 480000 == info[2]
    assert 2 == info[3]

    peak = a.get_peak(info)
    assert -0.7 == round(peak,1)

    lufs = a.get_luf(info)
    assert -4.7 == round(lufs,1)

#Two Channel - 24-bit Wave file
def test_One_8():
    a = ac('testfiles/2_Channel_24_48_minus6db.wav')
    info = a.open_wav_file()
    assert 48000 == info[1]
    assert 480000 == info[2]
    assert 2 == info[3]

    peak = a.get_peak(info)
    assert -0.7 == round(peak,1)

    lufs = a.get_luf(info)
    assert -4.7 == round(lufs,1)

#Two Channel - 16-bit Wave file
def test_One_8():
    a = ac('testfiles/Adele.wav')
    info = a.open_wav_file()
    assert 44100 == info[1]
    assert 11986380 == info[2]
    assert 2 == info[3]

    peak = a.get_peak(info)
    assert -0.4 == round(peak,1)

    lufs = a.get_luf(info)
    assert -8.5 == round(lufs,1)

#Two Channel - 24-bit mp4 file
def test_One_8():
    a = ac('2_Channel_24_48_minus6db.mp4')
    info = a.open_wav_file()
    assert 44100 == info[1]
    assert 443205 == info[2]
    assert 2 == info[3]

    peak = a.get_peak(info)
    assert -1.2 == round(peak,1)

    lufs = a.get_luf(info)
    assert -5.5 == round(lufs,1)
