from bs4 import BeautifulSoup
import requests
import json
import argparse
import os
import pathlib
from segment import Segment


    # url = 'https://theinfosphere.org/Transcript:Space_Pilot_3000'


def parse_time(time_id):
    return time_id[len('time-'):].split('-')

def get_segments_from_url(url: str):
    print("OPENING URL " + url)
    page = requests.get(url)

    # Init soup
    soup = BeautifulSoup(page.text, "html.parser")
    # transcript = soup.find("div", {"class": "mw-parser-output"})
    transcript = soup.find("div", {"id": "bodyContent"})
    sections = transcript.find_all("div", {"class": "poem"})

    # Parsing vars
    segments = []
    last_cleaned_text = 'NO TEXT SET'
    last_speaker = 'NO_SPEAKER_SET'
    last_time = [-1, -1]
    # Lags behind the sections by one section to roughly chop up the sections by timestamp
    for section in sections:
        if not (section.p.span):
            print("WARNING: Section without timestamp.")
            print("SKIPPING SEGMENT")
            print(section.p)
            print("CONTINUING")
            continue
        
        # Timestamp ([m, s])
        current_time = parse_time(section.p.span['id'])

        # Update segments
        if last_time != [-1, -1]:
            segment = Segment(last_speaker, last_cleaned_text, last_time[0], last_time[1], current_time[0], str(int(current_time[1])-1))
            segments.append(segment) 
            print("SEGMENT: " + str(segment))

        # Set last time regardless of whether it's the first run or not
        last_time = current_time

        # Speaker
        last_speaker = section.p.b.text
        
        # ????
        speaker_section = section.p.find('b')
        speaker_section.extract()
        
        print("SECTION: " + section.p.span['id'])
        time_section = section.p.span
        time_section.extract()
        
        # TODO: ???? i forgor

        # Text
        last_cleaned_text = section.p.text.rstrip()[2:]
    
    return segments

def write_segments(url: str, segment_output_filename: pathlib.Path):
    segments = get_segments_from_url(url)
    with open(segment_output_filename, "w+") as f:
        f.write(json.dumps(segments, default=(lambda x: x.__dict__ )))
    print("Output saved to " + segment_output_filename)

def main():
    parser = argparse.ArgumentParser(
                    prog='Transcript Scrape and Transform CLI',
                    description='Read transcripts and transform them into Segment data.')
                    # epilog='Text at the bottom of help')

    parser.add_argument('-t', '--transcript',
                       type=pathlib.Path,
                       default='transcripts.txt')
    
    parser.add_argument('output_dir', help='Path to generate segments folder in.', nargs='?', default='segment_data')

    
    args = parser.parse_args()

    # Output dir check/creation
    if os.path.exists(args.output_dir):
        raise Exception('ERROR: output_dir already exists.')
    else:
        os.mkdir(args.output_dir)

    with open(args.transcript, 'r') as f:
        for line in f:
            [full_filename, url] = line.strip().split('|')
            filename = full_filename.split('.')[0]
            write_segments(url, os.path.join(args.output_dir, filename + "_segments.json"))
            print(filename)
            print(url)

if __name__ == '__main__':
    main()

# Run w/ hardcoded args
# segments = get_segments()
# with open("seg_out.json", "w+") as f:
#     f.write(json.dumps(segments, default=(lambda x: x.__dict__ )))
#     #for segment in segments:
#     #    f.write(json.dumps(segment.__dict__))
# print("Output saved to seg_out.json")