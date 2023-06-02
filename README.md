# future-tts

Prepares data for and uses [Coqui AI](https://github.com/coqui-ai/TTS) for speech synthesis.

Could be used with other AI that use the LJ Speech Dataset. See:
  * https://tts.readthedocs.io/en/latest/formatting_your_dataset.html
  * https://keithito.com/LJ-Speech-Dataset/

## clip.py
Breaks apart source .wav files using metadata from a custom BeautifulSoup web parser. Has a CLI interface.

## scrape.py
Custom BeautifulSoup transcript parsing for this project. Not yet standardized for other custom TTS implementations.
