# Futurama TTS Data Preparation Example

This example demonstrates how to script the scraping and clipping of Futurama episode transcripts from The Infosphere and prepare them for TTS training.

## Step 1: Prepare the transcripts list

Create a `transcripts.txt` file with lines in the format:

```
episode1.wav|https://theinfosphere.org/Transcript:Space_Pilot_3000
episode2.wav|https://theinfosphere.org/Transcript:Episode_2
```

You can generate this list by scraping the episode transcript URLs from https://theinfosphere.org/Episode_Transcript_Listing.

## Step 2: Download or place your raw audio files

Place your raw `.wav` files in the `raw_wavs/` directory. The filenames should match those in `transcripts.txt` (e.g., `episode1.wav`).

## Step 3: Scrape and segment the transcripts

Run the following command from the `examples/futurama/` directory:

```bash
python ../../scrape.py -t transcripts.txt segment_data
```

This will create segment JSON files in `segment_data/`.

## Step 4: Clip the audio segments

Run the following command:

```bash
python ../../clip.py raw_wavs segment_data -o clips_output
```

This will create subdirectories in `clips_output/` with the segmented audio clips and metadata.

---

## Automating the Workflow

You can automate the entire workflow with a shell script (e.g., `run_pipeline.sh`):

```bash
#!/bin/bash
# 1. Scrape and segment transcripts
echo "Scraping and segmenting transcripts..."
python ../../scrape.py -t transcripts.txt segment_data

# 2. Clip audio segments
echo "Clipping audio segments..."
python ../../clip.py raw_wavs segment_data -o clips_output
```

Make sure to place your `transcripts.txt` and raw `.wav` files in the correct locations before running the script.
