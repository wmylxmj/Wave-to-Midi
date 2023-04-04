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

### Make the sound font file
To play the midi, a sound font of sine wave is needed. 
The .wav file of the sine wave can be obtained from wavSF.py and you can make the sound font file by [polyphone]https://www.polyphone-soundfonts.com/.

***

### Set the sound font
OmniMidi[https://github.com/KeppySoftware/OmniMIDI/releases] is recommended to set the sound font.
