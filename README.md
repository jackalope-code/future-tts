# future-tts

Prepares data for and uses [Coqui AI](https://github.com/coqui-ai/TTS) for speech synthesis.

Could be used with other AI that use the LJ Speech Dataset. See:
  * https://tts.readthedocs.io/en/latest/formatting_your_dataset.html
  * https://keithito.com/LJ-Speech-Dataset/

## clip.py
WIP
Has a CLI interface. Breaks apart source .wav files using a .json file containing an array of Segment data. This is created from scrape.py from a custom BeautifulSoup web parser.

## scrape.py
WIP
Custom BeautifulSoup transcript parsing for this project. Not yet standardized for other custom TTS implementations.

## TODO:
Segments are bugged on the second folder

AI training test

either multi voice training or filtering. somehow exact speakers must be specified.

output dir is created even on errors

clip.py should use default dirs
