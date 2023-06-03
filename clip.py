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

# TODO: implement ignore behavior
class IgnoreBehavior(Enum):
    REMOVE_GROUP = 0,
    SKIP = 1,
    IGNORED_ONLY = 2,
    NO_SKIPS = 3,
    REMOVE_SYMBOLS = 4

# input args: filename, segment file, output directory path
# outputs: segmented files in the specified output directory (directory should already exist for now)

class InputClipper:
    def __init__(self, wav_dir, segment_dir, output_dir, metadata_filename="metadata.txt") -> None:
        self.wav_dir= wav_dir
        self.segment_dir = segment_dir
        self.output_dir = output_dir
        self.metadata = ''
        self.metadata_filename = metadata_filename
    
    def _clip(self, subdir_name, wav_path, segment: Segment, saveMetadata=True):
        timestamp_start: int = int(segment['minuteStart'])*60 + int(segment['secondStart'])
        timestamp_end: int = int(segment['minuteStop'])*60 + int(segment['secondStop'])
        name = f"{segment['minuteStart']}.{segment['secondStart']}-{segment['minuteStop']}.{segment['secondStop']}_speaker={segment['speaker']}.wav"
        # read the file and get the sample rate and data
        # TODO: refactor out to clip_segments as a possible speed improvement?
        print("CUT WAV " + wav_path)
        rate, data = wavfile.read(wav_path) 


        duration = data.shape[0] / rate

        # get the frame to split at
        frame_start = round(rate * (0 if timestamp_start-10 < 0 else timestamp_start-10))

        frame_end = round(rate * (duration if timestamp_end+10 > duration else timestamp_end+10))

        # split
        clip = data[frame_start:frame_end]

        # subdir processing
        output_subdir = os.path.join(self.output_dir, subdir_name)
        if not os.path.exists(output_subdir):
            os.mkdir(output_subdir)
        # save the result
        wavfile.write(os.path.join(output_subdir, name), rate, clip)
        if saveMetadata:
            with open(os.path.join(output_subdir, self.metadata_filename), 'a') as meta_file:
                metadata = f"{name}|{segment['text']}"
                meta_file.write(metadata)
                meta_file.write('\n')
            

    def clip_segments(self, output_dir_name, wav_filename, segment_filename, ignore=None, skipOrRemove=IgnoreBehavior.SKIP):
        print('CLIP SEGMENTS: ', 'WAV FILE ', wav_filename, 'SEGMENT FILE ', segment_filename)
        full_segment_file_path = os.path.join(self.segment_dir, segment_filename)
        print("OPEN FILE " + full_segment_file_path)
        with open(full_segment_file_path, 'r') as f:
            contents = f.read()
            
            parsed: List[Segment] = json.loads(contents)#[json.loads(raw) for raw in contents]

            # TODO: BUG skipping any entries fucks up timestamps
            for entry in parsed:
                # entry = SimpleNamespace(**entry)
                print("READING " + str(f"{entry['speaker']} from {entry['minuteStart']}:{entry['secondStart']} to {entry['minuteStop']}:{entry['secondStop']}"))
                # break
                if skipOrRemove == IgnoreBehavior.REMOVE_GROUP:
                    raise NotImplementedError("IgnoreBehavior.REMOVE replacement regex behavior not implemented.")
                elif skipOrRemove == IgnoreBehavior.SKIP:
                    if any([re.search(x, entry['text']) for x in ignore]):
                        print("SKIPPING " + str(entry))
                        continue
                elif skipOrRemove == IgnoreBehavior.IGNORED_ONLY:
                    if not any([re.search(x, entry['text']) for x in ignore]):
                        continue
                self._clip(output_dir_name, wav_filename, entry)

# TODO: clip output dir is generated even if there's errors
# TODO: Test with fresh data to see if all folders are checked/accessed properly
def main():
    parser = argparse.ArgumentParser(
                    prog='InputClipper CLI',
                    description='Clip .wav files from Segment data.')
                    # epilog='Text at the bottom of help')
    
    # parser.add_argument('segment_dir', help='Segment file input directory.')
    parser.add_argument('wav_dir', help='Raw wav file input directory')
    parser.add_argument('segment_dir', help='Segment file input directory.', default='segment_data', nargs='?')
    parser.add_argument('-i', '--ignore-behavior', default='no_skips')
    parser.add_argument('-o', '--output-dir', help='Path to generate clips folder in.', default='', nargs='?')

    args = parser.parse_args()

    if args.ignore_behavior == 'skip':
        ignoreBehavior = IgnoreBehavior.SKIP
    elif args.ignore_behavior == 'remove':
        ignoreBehavior = IgnoreBehavior.REMOVE_GROUP
    elif args.ignore_behavior == 'ignored':
        ignoreBehavior = IgnoreBehavior.IGNORED_ONLY
    elif args.ignore_behavior == 'no_skips':
        ignoreBehavior = IgnoreBehavior.NO_SKIPS
    else:
        raise Exception('Unknown ignore behavior specified with -i. Valid options: skip (default) | remove | ignored')

    output_dir = args.output_dir if args.output_dir else f'output_{args.ignore_behavior}'

    if os.path.exists(output_dir):
        raise Exception('Cannot create directory ' + output_dir + ". Directory already exists.")
    else:
        os.mkdir(output_dir)

    # print(args)
    clipper = InputClipper(args.wav_dir, args.segment_dir, output_dir)
    # Iterate by segment and clip each into a directory
    for filename in os.listdir(args.segment_dir):
        name = filename.removesuffix('_segments.json')
        wav_filename = name + '.wav'
        # TODO: proper subdir here
        # output_subdir = os.path.join(output_dir, name)
        subdir = name
        wav_path = os.path.join(args.wav_dir, wav_filename)
        # TODO: BUG ignore nothing for now bc anything else fucks up timestamps
        clipper.clip_segments(subdir, wav_path, filename, ignore=['\[*\]'], skipOrRemove=ignoreBehavior)
        # clipper.clip_segments(output_subdir, wav_path, filename)

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