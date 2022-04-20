from audio_calculations import audio_calculations as ac


#One Channel 24-bit Wave File
def test_One_24():
    a = ac('testfiles/SineWave.wav')
    info = a.select_file()
    assert 48000 == info[1]
    assert 1 == info[2]

    assert -9.1 == round(info[3],1)

    assert -6.0 == round(info[4],1)
    
#One Channel 16-bit wave file
def test_One_16():
    a = ac('testfiles/BabyElephantWalk60.wav')
    info = a.select_file()
    assert 22050 == info[1]
    assert 1 == info[2]

    assert -23.1 == round(info[3],1)

    assert -5.3 == round(info[4],1)
    
#One Channel 8-bit wave file
def test_One_8():
    a = ac('testfiles/taunt.wav')
    info = a.select_file()
    assert 22257 == info[1]
    assert 1 == info[2]

    assert -12.1 == round(info[3],1)

    assert 0.6 == round(info[4],1)

#Two Channel - 24-bit Flac file
def test_Two_24_flac():
    a = ac('testfiles/2_Channel_24_48_minus6db.flac')
    info = a.select_file()
    assert 48000 == info[1]
    assert 2 == info[2]

    assert -4.8 == round(info[3],1)

    assert -0.6 == round(info[4],1)

#Two Channel - 24-bit Wave file
def test_Two_24():
    a = ac('testfiles/2_Channel_24_48_minus6db.wav')
    info = a.select_file()
    assert 48000 == info[1]
    assert 2 == info[2]

    assert -4.8 == round(info[3],1)

    assert -0.6 == round(info[4],1)

#Two Channel - 16-bit Wave file
def test_Two_16():
    a = ac('testfiles/Adele.wav')
    info = a.select_file()
    assert 44100 == info[1]
    assert 2 == info[2]

    assert -8.5 == round(info[3],1)

    assert -0.4 == round(info[4],1)

#Two Channel - 24-bit mp4 file
def test_Two_24_mp4():
    a = ac('testfiles/2_Channel_24_48_minus6db.mp4')
    info = a.select_file()
    assert 44100 == info[1]
    assert 2 == info[2]

    assert -5.0 == round(info[3],1)

    assert -0.4 == round(info[4],1)
    
#Six Channel - 24-bit wave file
def test_Six_24_Wave():
    a = ac('testfiles/6_Channel_White_Noise.wav')
    info = a.select_file()
    assert 44100 == info[1]
    assert 6 == info[2]

    assert -5.0 == round(info[3],1)

    assert -6.0 == round(info[4],1)
