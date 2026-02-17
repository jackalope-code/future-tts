# Example Workflow: Scrape, Segment, and Clip Audio for TTS

This example demonstrates a typical pipeline for preparing data for TTS training using this repository.

## Directory Structure

- `examples/`
  - `transcripts.txt` — List of transcript URLs and output names
  - `raw_wavs/` — Directory for raw .wav files (placeholders)
  - `segment_data/` — Output directory for segment JSON files
  - `clips_output/` — Output directory for clipped audio

## Step 1: Scrape and Segment Transcripts

Prepare a `transcripts.txt` file in the `examples/` directory with lines like:

```
episode1.wav|https://theinfosphere.org/Transcript:Space_Pilot_3000
episode2.wav|https://theinfosphere.org/Transcript:Episode_2
```

Run the transcript scraper:

```bash
python ../scrape.py -t transcripts.txt segment_data
```

This will create segment JSON files in `segment_data/`.

## Step 2: Prepare Raw Audio

Place your raw `.wav` files in the `raw_wavs/` directory. The filenames should match those in `transcripts.txt` (e.g., `episode1.wav`).

## Step 3: Clip Audio Segments

Run the clipper to segment the audio:

```bash
python ../clip.py raw_wavs segment_data -o clips_output
```

This will create subdirectories in `clips_output/` with the segmented audio clips and metadata.

---

You can modify the ignore behavior or run single-file operations using the CLI options described in the main code documentation.
