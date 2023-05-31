from bs4 import BeautifulSoup
import requests
import json

from segment import Segment


url = 'https://theinfosphere.org/Transcript:Space_Pilot_3000'
page = requests.get(url)

soup = BeautifulSoup(page.text, "html.parser")
transcript = soup.find("div", {"class": "mw-parser-output"})
sections = transcript.find_all("div", {"class": "poem"});

def parse_time(time_id):
    return time_id[len('time-'):].split('-')

def get_segments():
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

# Run w/ hardcoded args
segments = get_segments()
with open("seg_out.json", "w+") as f:
    f.write(json.dumps(segments, default=(lambda x: x.__dict__ )))
    #for segment in segments:
    #    f.write(json.dumps(segment.__dict__))
print("Output saved to seg_out.json")