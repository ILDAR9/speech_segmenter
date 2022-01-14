# SpeechSegmenter

SpeechSegmenter is a CNN-based audio segmentation toolkit.


It splits audio signals into homogeneous zones of speech, music and noise.
Speech zones are split into segments tagged using speaker gender (male or female).
Male and female classification models are optimized for French language since they were trained using French speakers (accoustic correlates of speaker gender are language dependent).
Zones corresponding to speech over music or speech over noise are tagged as speech.


Based on research: 
"An Open-Source Speaker Gender Detection Framework for Monitoring Gender Equality".

This is a specific customisation of inaSpeechSegmenter.

## Installation

### Prerequisites

SpeechSegmenter requires ffmpeg for decoding any type of format.
Installation of ffmpeg for ubuntu can be done using the following commandline:
```bash
$ sudo apt-get install ffmpeg
```

### PIP installation
```bash
$ python3.8 -m venv tenv
$ source tenv/bin/activate
$ pip install -r requirements.txt
```

## Using SpeechSegmenter

### Speech Segmentation Program
Binary program scripts/speech_segmenter.py may be used to segment multimedia archives encoded in any format supported by ffmpeg. It requires input media and output csv files corresponding to the segmentation. Corresponding csv may be visualised using softwares such as https://www.sonicvisualiser.org/
```bash
# get help
$ python -m scripts.speech_segmenter --help
usage: python -m scripts.speech_segmenter [-h] -i INPUT [INPUT ...] -o OUTPUT_DIRECTORY [-d {sm,smn}] [-g {true,false}] [-b FFMPEG_BINARY] [-e {csv,textgrid}]

Do Speech/Music(/Noise) and Male/Female segmentation and store segmentations into CSV files. Segments labelled 'noEnergy' are discarded from music, noise, speech and gender
analysis. 'speech', 'male' and 'female' labels include speech over music and speech over noise. 'music' and 'noise' labels are pure segments that are not supposed to contain speech.

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT [INPUT ...], --input INPUT [INPUT ...]
                        Input media to analyse. May be a full path to a media (/home/david/test.mp3), a list of full paths (/home/david/test.mp3 /tmp/mymedia.avi), a regex input
                        pattern ("/home/david/myaudiobooks/*.mp3"), an url with http protocol (http://url_of_the_file)
  -o OUTPUT_DIRECTORY, --output_directory OUTPUT_DIRECTORY
                        Directory used to store segmentations. Resulting segmentations have same base name as the corresponding input media, with csv extension. Ex: mymedia.MPG will
                        result in mymedia.csv
  -d {sm,smn}, --vad_engine {sm,smn}
                        Voice activity detection (VAD) engine to be used (default: 'smn'). 'smn' split signal into 'speech', 'music' and 'noise' (better). 'sm' split signal into
                        'speech' and 'music' and do not take noise into account, which is either classified as music or speech. Results presented in ICASSP were obtained using 'sm'
                        option
  -g {true,false}, --detect_gender {true,false}
                        (default: 'true'). If set to 'true', segments detected as speech will be splitted into 'male' and 'female' segments. If set to 'false', segments
                        corresponding to speech will be labelled as 'speech' (faster)
  -b FFMPEG_BINARY, --ffmpeg_binary FFMPEG_BINARY
                        Your custom binary of ffmpeg
  -e {csv,textgrid}, --export_format {csv,textgrid}
                        (default: 'csv'). If set to 'csv', result will be exported in csv. If set to 'textgrid', results will be exported to praat Textgrid

```
### Using Speech Segmentation API

SpeechSegmentation API is intended to be very simple to use.
The class allowing to perform segmentations is called Segmenter.
It is the only class that you need to import in a program.
Class constructor accept 3 optional arguments:
* vad_engine (default: 'smn'). Allows to choose between 2 voice activity detection engines.
  * 'smn' is the more recent engine and splits signal into speech, music and noise segments
  * 'sm' was not trained with noise examples, and split signal into speech and music segments. Noise segments are either considered as speech or music. This engine was used in ICASSP study, and won MIREX 2018 speech detection challenge.
* detect_gender (default: True): if set to True, performs gender segmentation on speech segment and outputs labels 'female' or 'male'. Otherwise, outputs labels 'speech' (faster).
* ffmpeg: allows to provide a specific binary of ffmpeg instead of default system installation


See the following notebook for a comprehensive example: [API Tutorial Here!](API_Tutorial.ipynb)