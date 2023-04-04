# Wave-to-Midi
A tool for converting .wav to .midi

***

First, convert the audio to .wav file.
```
ffmpeg -i input.mp3 -f wav output.wav
```

***
Then set the file path in wav2midi.py and run the program, you will get a midi file.

***
To play the midi, we need to set the sound font to sine wave

***
OmniMidi is recommended to set the sound font.
> https://github.com/KeppySoftware/OmniMIDI/releases
