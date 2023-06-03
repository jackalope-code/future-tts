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
- AI training test
- Merge and filter pipeline?
- Process segments and clips so that sections can be skipped through arbitrarily.
- Add speaker filtering when working with clips/segments?? Merge/filter pipeline may make this unnecessary.


## BUGS
- output dir is created even on errors
- There's more bugs in comments
