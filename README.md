# future-tts

Prepares data for and uses [Coqui AI](https://github.com/coqui-ai/TTS) for speech synthesis.

Could be used with other AI that use the LJ Speech Dataset. See:
  * https://tts.readthedocs.io/en/latest/formatting_your_dataset.html
  * https://keithito.com/LJ-Speech-Dataset/

WIP
## clip.py
Has a CLI interface. Breaks apart source .wav files using a .json file containing an array of Segment data. This is created from scrape.py from a custom BeautifulSoup web parser.

WIP
## scrape.py
Custom BeautifulSoup transcript parsing for this project. Not yet standardized for other custom TTS implementations.
