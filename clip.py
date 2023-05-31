from typing import List
from types import SimpleNamespace
from enum import Enum
from scipy.io import wavfile
import os
import json
import re
from segment import Segment

# the timestamp to split at (in seconds)
#first_timestamp = 1195.1 #102.0 incorrect #221.0 incorrect #24.6

#second_timestamp = 1196.8 #106.9 incorrect #224.1 incorrect #28.0

class IgnoreBehavior(Enum):
    REMOVE = 0,
    SKIP = 1,
    KEEP_ONLY = 2

# input args: filename, segment file, output directory path
# outputs: segmented files in the specified output directory (directory should already exist for now)

class InputClipper:
    def __init__(self, source_filename, segment_filename, output_dir) -> None:
        self.source_filename = source_filename
        self.segment_filename = segment_filename
        self.output_dir = output_dir
    
    def _clip(self, segment: Segment):
        timestamp_start: int = int(segment['minuteStart'])*60 + int(segment['secondStart'])
        timestamp_end: int = int(segment['minuteStop'])*60 + int(segment['secondStop'])
        name = f"start={timestamp_start:.1f}s stop={timestamp_end:.1f}s speaker_{segment['speaker']}.wav"
        # read the file and get the sample rate and data
        rate, data = wavfile.read(self.source_filename) 

        # get the frame to split at
        frame_start = round(rate * timestamp_start)

        frame_end = round(rate * timestamp_end)

        # split
        clip = data[frame_start:frame_end]

        # save the result
        wavfile.write(os.path.join(self.output_dir, name), rate, clip)

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
                elif skipOrRemove == IgnoreBehavior.KEEP_ONLY:
                    if not any([re.search(x, entry['text']) for x in ignore]):
                        continue
                
                self._clip(entry)
        
def test():
    source = "../test.wav"
    segments = "seg_out.json"
    output_dir = "output_ignores"
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)
    clipper = InputClipper(source, segments, output_dir)
    clipper.clip_segments(ignore=['\[*\]'], skipOrRemove=IgnoreBehavior.KEEP_ONLY)


test()