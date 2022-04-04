from audio_calculations import audio_calculations as ac

def test_wavFileOneChannel():
    a = ac('SineWave.wav')
    info = a.open_wav_file()
    assert 48000 == info[1]
    assert 480000 == info[2]
    assert 1 == info[3]

    peak = a.get_peak(info)
    assert -5.995 == round(peak,3)

    lufs = a.get_luf(info)
    assert -9.045 == round(lufs,3)

def test_flacFileMultChannels():
    a = ac('2_Channel_24_48_minus6db.flac')
    info = a.open_wav_file()
    assert 48000 == info[1]
    assert 480000 == info[2]
    assert 2 == info[3]

    peak = a.get_peak(info)
    assert -0.738 == round(peak,3)

    lufs = a.get_luf(info)
    assert -4.659 == round(lufs,3)