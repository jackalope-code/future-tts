@echo off
REM 1. Scrape and segment transcripts
echo Scraping and segmenting transcripts...
python ../../scrape.py -t transcripts.txt segment_data

REM 2. Clip audio segments
echo Clipping audio segments...
python ../../clip.py raw_wavs segment_data -o clips_output
