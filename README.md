# Wave-to-Midi
.wav到.mid的转换工具

***

### 转换midi文件
首先使用ffmpeg工具将任意格式的音频转为wav文件，例如.mp3转.wav
```
ffmpeg -i input.mp3 -f wav output.wav
```
然后在wav2midi.py中设置文件输入输出路径，运行程序得到midi文件

***

### 制作正弦波音源
由于时频转换的基波为正弦波，因此要还原音频的声音，音源一定要使用正弦波
可以由wavSF.py生成正弦波的wav文件然后通过[Polyphone](https://www.polyphone-soundfonts.com/)来制作音源文件.

***

### 设置音源
推荐[OmniMidi](https://github.com/KeppySoftware/OmniMIDI/releases)来设置音源.

***

###推荐的midi播放器
- [MIDITrail](http://miditrail.osdn.jp/Windows/MANUAL.en.html)
- [Kiva](https://github.com/arduano/Kiva)
