# -*- coding: utf-8 -*-
"""
Created on Sun Apr  2 17:14:35 2023

@author: wmy
"""

import os
import wave
import librosa
import librosa.display
import python3_midi as midi
import music21
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import Audio
from tqdm import tqdm

y, sr = librosa.load(r'test4.wav', sr=None)
print("Sample Rate: {}".format(sr))

Audio(data=y, rate=sr)

# settings
hop_length = 512

y_harmonic, y_percussive = librosa.effects.hpss(y)
tempo, beat_frames = librosa.beat.beat_track(y=y_percussive, sr=sr, hop_length=hop_length)
beat_times = librosa.frames_to_time(beat_frames, sr=sr, hop_length=hop_length)
print("BPM: {}".format(tempo))

Audio(data=y_harmonic, rate=sr)

Audio(data=y_percussive, rate=sr)

CQT = librosa.cqt(y, sr=sr, hop_length=hop_length, fmin=librosa.note_to_hz('A0'), n_bins=88, bins_per_octave=12)
C = np.abs(CQT)
C_dB = librosa.amplitude_to_db(C, ref=np.max)

idx = tuple([slice(None), slice(*list(librosa.time_to_frames([0, 5], sr=sr, hop_length=hop_length)))])
fig, ax = plt.subplots()
img = librosa.display.specshow(C_dB[idx], sr=sr, hop_length=hop_length, y_axis='cqt_note', x_axis='time', \
                               fmin=librosa.note_to_hz('A0'), fmax=librosa.note_to_hz('C8'))
ax.set_title('Constant-Q power spectrum')
fig.colorbar(img, ax=ax, format="%+2.0f dB")

# 轨道数
num_tracks = 16
# 截断音量 （dB）
cutoff_power = -70
# 最短音符 8分 16分 32分
unit_note = 16

class PianoTrack(object):
    
    def __init__(self, unit_note, tempo):
        self.__lowest_pitch = 21
        self.__highest_pitch = 108
        self.__pitch_span = 88
        mm = music21.tempo.MetronomeMark()
        mm.setQuarterBPM(tempo)
        self.streams = [music21.stream.Stream(mm) for x in range(self.__pitch_span)]
        self.notestate = np.array([0 for x in range(self.__pitch_span)])
        self.noteduration = np.array([0 for x in range(self.__pitch_span)])
        self.notevelocity = np.array([0 for x in range(self.__pitch_span)])
        self.unit_note = unit_note
        pass
    
    def note_on(self, pitch, velocity):
        note_i = pitch - self.__lowest_pitch
        # 纵连
        if self.notestate[note_i] == 1:
            note = music21.note.Note(pitch)
            note.duration.quarterLength = self.noteduration[note_i] * 4 / self.unit_note
            note.volume.velocity = self.notevelocity[note_i]
            self.streams[note_i].append(note)
            pass
        # 休止符
        elif self.noteduration[note_i] > 0:
            note = music21.note.Rest()
            note.duration.quarterLength = self.noteduration[note_i] * 4 / self.unit_note
            self.streams[note_i].append(note)
            pass
        self.notevelocity[note_i] = velocity
        self.notestate[note_i] = 1
        self.noteduration[note_i] = 0
        pass
    
    def note_off(self, pitch):
        note_i = pitch - self.__lowest_pitch
        if self.notestate[note_i] == 0:
            return
        note = music21.note.Note(pitch)
        note.duration.quarterLength = self.noteduration[note_i] * 4 / self.unit_note
        note.volume.velocity = self.notevelocity[note_i]
        self.streams[note_i].append(note)
        self.notestate[note_i] = 0
        self.noteduration[note_i] = 0
        pass
    
    def update(self):
        self.noteduration = self.noteduration + 1
        pass
    
    pass


beat_frames = beat_frames.tolist()
while beat_frames[0] - (beat_frames[1] - beat_frames[0]) >= 0:
    beat_frames.insert(0, beat_frames[0] - (beat_frames[1] - beat_frames[0]))
    pass
while beat_frames[-1] + (beat_frames[-1] - beat_frames[-2]) < C_dB.shape[-1]:
    beat_frames.append(beat_frames[-1] + (beat_frames[-1] - beat_frames[-2]))
    pass
beat_frames = np.array(beat_frames)

piano_lowest_pitch = 21
piano_pitch_span = 88
pitch_span = piano_pitch_span
tracks = [PianoTrack(unit_note, tempo) for x in range(num_tracks)]
prevpower = np.array([np.min(C_dB.T) for x in range(pitch_span)])
prevamplitude = np.array([np.min(C.T) for x in range(pitch_span)])
for beati in tqdm(range(len(beat_frames)-1)):
    bsframe = beat_frames[beati]
    beframe = beat_frames[beati+1]
    duration = (beframe - bsframe) * 4 / unit_note
    for i in range(unit_note//4):
        nsframe = bsframe + int(i * duration + 0.5)
        neframe = bsframe + int((i+1) * duration + 0.5)
        power = np.max(C_dB.T[nsframe:neframe, :], axis=0)
        amplitude = np.max(C.T[nsframe:neframe, :], axis=0)
        for notei in reversed(range(pitch_span)):
            n = power[notei]
            p = prevpower[notei]
            if (n - p) <= -3:
                pitch = notei + piano_lowest_pitch
                for track in tracks:
                    track.note_off(pitch)
                    pass
                pass
            elif (n - p) > 0 and n >= cutoff_power:
                pitch = notei + piano_lowest_pitch
                for track in tracks:
                    track.note_off(pitch)
                    pass
                velocity = int(127 * amplitude[notei] ** 0.5 / np.max(C.T) ** 0.5)
                track_index = min(num_tracks-1, int((power[notei] - cutoff_power) / ((0 - cutoff_power) / num_tracks)))
                tracks[track_index].note_on(pitch, velocity)
                pass
            pass
        for track in tracks:
            track.update()
            prevpower = power
            prevamplitude = amplitude
            pass
        pass
    pass      

mf = music21.midi.MidiFile()
parti = 1
for track in tqdm(tracks[::-1]):
    part = music21.stream.Part(track.streams).chordify()
    miditrack = music21.midi.translate.streamHierarchyToMidiTracks(part, acceptableChannelList=[parti])
    if parti == 1:
        mf.tracks.append(miditrack[0])
        mf.tracks.append(miditrack[1])
        pass
    else:
        mf.tracks.append(miditrack[1])
        pass
    parti += 1
    pass

mf.open(r'test4_512.mid', 'wb') 
mf.write() 
mf.close() 