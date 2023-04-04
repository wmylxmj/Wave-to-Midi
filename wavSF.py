# -*- coding: utf-8 -*-
"""
Created on Tue Apr  4 16:28:57 2023

@author: wmy
"""

import numpy as np
import librosa
from scipy.io import wavfile

sr = 44100
duration = 5
amplitude = 16000

for pitch in range(128):
    frequency = librosa.midi_to_hz(pitch)
    period = 1 / frequency
    t = np.linspace(0, duration, sr * duration)
    y = np.sin(frequency * 2 * np.pi * t)
    y = np.rint(amplitude * y)
    y = np.int16(y)
    wavfile.write('sine wave/sine wave pitch {}.wav'.format(pitch), sr, y)
    pass
