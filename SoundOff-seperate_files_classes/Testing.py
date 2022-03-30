import pytest

from main import App

def test_luf():
    a=App()
    
    filename='SineWave.wav'
    a.change_file_path(filename)
    wave_info=a.open_wav_file()
    assert -9.045 == round(a.get_luf(wave_info),3)
    

def test_peak():
    a=App()
    filename='SineWave.wav'
    a.change_file_path(filename)
    wave_info=a.open_wav_file()
    assert -5.995 == round(a.get_peak(wave_info),3)