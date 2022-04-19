from audio_calculations import audio_calculations as ac


def test_file(file,rate, length_file,n_channels,assert_peak, assert_lufs):
    a = ac(file)
    info = a.open_wav_file()
    assert rate == info[1]
    assert length_file == info[2]
    assert n_channels == info[3]

    peak = a.get_peak(info)
    assert assert_peak == round(peak,1)

    lufs = a.get_luf(info)
    assert assert_lufs == round(lufs,1)


#One channel wave files

#24-bit
test_file('SineWave.wav',48000,480000,1,-6.0,-9.0)

#16-bit
test_file('testfiles/BabyElephantWalk60.wav',22050,1323000,1,-5.3,-22.9)

#8-bit
test_file('testfiles/taunt.wav',22257,91240,1,0.6,-11.5)

#Two Channel files

#flac - 24-bit
test_file('2_Channel_24_48_minus6db.flac',48000,480000,2,-0.7,-4.7)

#wav - 24-bit
test_file('testfiles/2_Channel_24_48_minus6db.wav',48000,480000,2,-0.7,-4.7)

#wav - 16-bit
test_file('testfiles/Adele.wav',44100,11986380,2,-0.4,-8.5)

#mp4 - 24-bit
test_file('2_Channel_24_48_minus6db.mp4',44100,443205,2,-1.2,-5.5)


