# Wave-to-Midi
A tool for converting .wav to .midi

***

### Generate the midi file
First, convert the audio to .wav file.
```
ffmpeg -i input.mp3 -f wav output.wav
```
Then set the file path in wav2midi.py and run the program, you will get a midi file.

***
### Set the sound font
To play the midi, a sound font of sine wave is needed

OmniMidi is recommended to set the sound font.
> https://github.com/KeppySoftware/OmniMIDI/releases
