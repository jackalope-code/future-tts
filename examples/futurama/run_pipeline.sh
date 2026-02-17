#!/bin/bash
# 1. Scrape and segment transcripts
echo "Scraping and segmenting transcripts..."
PYDIR="$(cd "$(dirname "$0")" && cd ../.. && pwd)"
EXDIR="$(cd "$(dirname "$0")" && pwd)"
python "$PYDIR/scrape.py" -t "$EXDIR/transcripts.txt" "$EXDIR/segment_data"

# 2. Clip audio segments
echo "Clipping audio segments..."
python "$PYDIR/clip.py" "$EXDIR/raw_wavs" "$EXDIR/segment_data" -o "$EXDIR/clips_output"
