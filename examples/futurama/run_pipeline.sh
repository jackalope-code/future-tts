#!/bin/bash
# 1. Scrape and segment transcripts
echo "Scraping and segmenting transcripts..."
python ../../scrape.py -t transcripts.txt segment_data

# 2. Clip audio segments
echo "Clipping audio segments..."
python ../../clip.py raw_wavs segment_data -o clips_output
