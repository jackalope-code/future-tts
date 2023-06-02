from typing import List
from types import SimpleNamespace
from enum import Enum
from scipy.io import wavfile
import os
import json
import re
from segment import Segment
import sys
import argparse

# the timestamp to split at (in seconds)
#first_timestamp = 1195.1 #102.0 incorrect #221.0 incorrect #24.6

#second_timestamp = 1196.8 #106.9 incorrect #224.1 incorrect #28.0

class IgnoreBehavior(Enum):
    REMOVE = 0,
    SKIP = 1,
    IGNORED_ONLY = 2

# input args: filename, segment file, output directory path
# outputs: segmented files in the specified output directory (directory should already exist for now)

class InputClipper:
    def __init__(self, source_filename, segment_filename, output_dir, metadata_filename="metadata.txt") -> None:
        self.source_filename = source_filename
        self.segment_filename = segment_filename
        self.output_dir = output_dir
        self.metadata = ''
        self.metadata_filename = metadata_filename
    
    def _clip(self, segment: Segment, saveMetadata=True):
        timestamp_start: int = int(segment['minuteStart'])*60 + int(segment['secondStart'])-1
        timestamp_end: int = int(segment['minuteStop'])*60 + int(segment['secondStop'])+1
        name = f"{timestamp_start}-{timestamp_end}s_speaker={segment['speaker']}.wav"
        # read the file and get the sample rate and data
        rate, data = wavfile.read(self.source_filename) 

        # get the frame to split at
        frame_start = round(rate * timestamp_start)

        frame_end = round(rate * timestamp_end)

        # split
        clip = data[frame_start:frame_end]

        # save the result
        wavfile.write(os.path.join(self.output_dir, name), rate, clip)
        if saveMetadata:
            with open(os.path.join(self.output_dir, self.metadata_filename), 'a') as meta_file:
                metadata = f"{name}|{segment['text']}"
                meta_file.write(metadata)
                meta_file.write('\n')
            

    def clip_segments(self, ignore=None, skipOrRemove=IgnoreBehavior.SKIP):
        with open(self.segment_filename, 'r') as f:
            contents = f.read()
            
            parsed: List[Segment] = json.loads(contents)#[json.loads(raw) for raw in contents]

            for entry in parsed:
                # entry = SimpleNamespace(**entry)
                print("READING " + str(f"{entry['speaker']} from {entry['minuteStart']}:{entry['secondStart']} to {entry['minuteStop']}:{entry['secondStop']}"))
                # break
                if skipOrRemove == IgnoreBehavior.REMOVE:
                    raise NotImplementedError("IgnoreBehavior.REMOVE replacement regex behavior not implemented.")
                elif skipOrRemove == IgnoreBehavior.SKIP:
                    if any([re.search(x, entry['text']) for x in ignore]):
                        print("SKIPPING " + str(entry))
                        continue
                elif skipOrRemove == IgnoreBehavior.IGNORED_ONLY:
                    if not any([re.search(x, entry['text']) for x in ignore]):
                        continue
                
                self._clip(entry)

def main():
    parser = argparse.ArgumentParser(
                    prog='InputClipper CLI',
                    description='Clip .wav files from Segment data.')
                    # epilog='Text at the bottom of help')

    parser.add_argument('input_directory', help='Transcript file input directory.')
    parser.add_argument('output_dir', help='Path to generate clips folder in.')

    args = parser.parse_args()

    clip_dir = os.path.join(args.output_dir, 'clips')
    if os.path.exists(clip_dir):
        raise Exception('Cannot create directory ' + clip_dir + ". Directory already exists.")
    else:
        os.mkdir(clip_dir)

    

    print(args)

if __name__ == "__main__":
    main()

# def test():
#     source = "../test.wav"
#     segments = "seg_out.json"
#     output_dir = "output_ignores"
#     if not os.path.isdir(output_dir):
#         os.makedirs(output_dir)
#     clipper = InputClipper(source, segments, output_dir)
#     clipper.clip_segments(ignore=['\[*\]'], skipOrRemove=IgnoreBehavior.IGNORED_ONLY)


# test()