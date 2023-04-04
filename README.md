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
OmniMidi is recommended to set the soundfont.\n
https://github.com/KeppySoftware/OmniMIDI/releases
